import requests, time, random
import pandas as pd
import numpy as np
import sys
import subprocess 
import os

# === Configuration ===
#URL = "http://192.168.50.1:8000"  # Matches your FastAPI endpoint
#URL = "http://172.20.10.3:8000" # local host for testing

# my wifi at home
# using ngrok
URL = "https://owners-league.com"



def update_stats(year: str ="2024"):
    """ Funcation to update the stats of the NFL Teams"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        )
    }
    url = f"https://www.espn.com/nfl/fpi/_/view/projections/season/{year}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text
    dfs = pd.read_html(html_content)
    df = pd.concat([dfs[0], dfs[1]], axis=1)
    return df


def add_team_stats(league_df: pd.DataFrame, df:pd.DataFrame):
    out = league_df.copy()  # work on a copy
    for i in range(0, len(league_df)):
        total_wins = 0
        total_losses = 0
        total_ties = 0
        total_sb_pct = 0.0
        total_proj_wins = 0.0
        for j, team in enumerate(out["teams"][i]):
            
            # create new columns with team info
            out.at[i, f"team_{j+1}"]   = team
            wlt = df.loc[df["Team"] == team, "W-L-T"].iat[0].split("-")
            wins, losses, ties = map(int, wlt)
            out.at[i, f"wins_{j+1}"]   = wins
            out.at[i, f"losses_{j+1}"] = losses
            out.at[i, f"ties_{j+1}"]   = ties

            # now compute winning % = (wins + 0.5*ties) / total games
            total_wins += wins
            total_losses += losses
            total_ties += ties
            games = wins + losses + ties
            pct   = (wins + ties*0.5) / games if games else 0.0

            out.at[i, f"pct_{j+1}"]    = pct 
            proj_wins = float(df.loc[df["Team"] == team, "PROJ W-L"].iat[0].split("-")[0])
            total_proj_wins += proj_wins
            out.at[i, f"proj_win_{j+1}"] = proj_wins

            # calculate suber bowl %
            sb_pct = float(df.loc[df["Team"] == team, "WIN SB%"].iat[0])
            total_sb_pct += sb_pct
            out.at[i, f"sb_pct_{j+1}"] = sb_pct
        
        # compute the % for each owner
        total_games = total_wins + total_losses + total_ties
        total_pct = (total_wins + total_ties*0.5) / total_games if total_games else 0.0
        out.at[i, "total_wins"]   = total_wins
        out.at[i, "total_losses"] = total_losses
        out.at[i, "total_ties"]   = total_ties
        out.at[i, "total_pct"]    = total_pct
        out.at[i, "total_sb_pct"]    = total_sb_pct
        out.at[i, "total_proj_wins"] = total_proj_wins

    return out

def simulate(stats_df):
    games = stats_df.iloc[0]["wins_1"] + stats_df.iloc[0]["losses_1"] + stats_df.iloc[0]["ties_1"]
    games = 8
    if games >= 17 :
        games = 17
    std = 1.5 * (17 - games) / 17
    std = 1.5 * (17 - 12) / 17 # add some variation for now
    var = 3 * std**2
    means = stats_df["total_wins"].values
    number = 10000
    sims = np.random.normal(loc=means, scale=np.sqrt(var), size=(number, means.size))
    # calculate win percentages
    max_indices = np.argmax(sims, axis=1)
    counts = np.bincount(max_indices, minlength=sims.shape[1])
    percentages = counts / sims.shape[0]
    # add percetanges to the dataframe
    stats_df["league_win_pct"] = percentages 


### FFT transforms
def owner_pmf(team_ps, team_games, M=None):
    # force total_games to be a Python int
    total_games = int(sum(team_games))

    if M is None:
        # now bit_length() works
        M = 1 << ((total_games*2 - 1).bit_length())

    omega = 2*np.pi*np.arange(M)/M

    cf = np.ones(M, dtype=complex)
    for p, N in zip(team_ps, team_games):
        single_game = (1-p) + p*np.exp(1j*omega)
        cf *= single_game**int(N)   # N should already be int

    pmf = np.fft.ifft(cf).real
    pmf = np.maximum(pmf, 0)
    pmf /= pmf.sum()
    return pmf[: total_games+1]

def owner_pmf_with_offset(team_ps, team_games, offset, M=None):
    total_future = int(sum(team_games))
    if M is None:
        M = 1 << ((total_future*2 - 1).bit_length())
    ω = 2*np.pi*np.arange(M)/M

    cf = np.ones(M, dtype=complex)
    for p_rem, N_rem in zip(team_ps, team_games):
        cf *= ((1-p_rem) + p_rem*np.exp(1j*ω))**N_rem

    # shift by the OFFSET = sum of current wins
    cf *= np.exp(1j * ω * offset)

    pmf = np.fft.ifft(cf).real
    pmf = np.maximum(pmf, 0)
    pmf /= pmf.sum()

    # final PMF length = current_wins + future_games + 1
    return pmf[: offset + total_future + 1]



def champ_probs(all_team_ps, owners):
    pmfs, max_len = [], 0
    # 1) build each owner's PMF
    for teams in owners:
        ps, gs = zip(*(all_team_ps[t] for t in teams))
        pmf = owner_pmf(ps, gs)
        pmfs.append(pmf)
        max_len = max(max_len, len(pmf))

    # 2) build CDFs
    cdfs = [ np.cumsum(np.pad(p, (0, max_len-len(p)))) for p in pmfs ]

    # 3) compute champion probabilities
    P = []
    n = len(pmfs)
    for j in range(n):
        pmf_j = np.pad(pmfs[j], (0, max_len - len(pmfs[j])))
        prob = 0.0
        # skip m=0 since Pr(others < 0)=0 anyway
        for m in range(1, max_len):
            # product of Pr(owner k has < m) for all k != j
            others_lt = np.prod([ cdfs[k][m-1] for k in range(n) if k != j ])
            prob += pmf_j[m] * others_lt
        P.append(prob)

    return P

def notify_with_sound(mp3_file="sound.mp3", bt_name="JBL Clip 4"):
    """Play an MP3 on a Bluetooth speaker (connects only if not already connected)."""
    if not os.path.isfile(mp3_file):
        print(f"❌ File not found: {mp3_file}")
        return

    try:
        # 1) power on
        subprocess.run(["bluetoothctl", "power", "on"], check=True)

        # 2) find MAC
        out = subprocess.check_output(["bluetoothctl", "devices"]).decode().splitlines()
        mac = next((line.split()[1] for line in out if bt_name in line), None)
        if not mac:
            print(f"Speaker '{bt_name}' not found.")
            return

        # 3) trust & connect only if needed
        subprocess.run(["bluetoothctl", "trust", mac], check=True)
        info = subprocess.check_output(["bluetoothctl", "info", mac]).decode()
        if "Connected: yes" not in info:
            print(f"Connecting to {bt_name}…")
            subprocess.run(["bluetoothctl", "connect", mac], check=True)
            time.sleep(2)

        # 4) play
        print(f"▶️ Playing {mp3_file}")
        subprocess.run(["mpg123", "-q", mp3_file], check=True)

    except subprocess.CalledProcessError as e:
        print("Bluetooth or playback error:", e)
    except Exception as e:
        print("Unexpected error:", e)




# === Main execution ===
if __name__ == "__main__":
    try:
        df = update_stats(*sys.argv[1:2])
        print("New ESPN data received!")


    except Exception as e:
        print("Failed to collect data from ESPN:", e)
    # Fetch league info from server
    try:
        league_response = requests.get(URL + "/league_info")
        league_response.raise_for_status()  # Ensure 200 OK
        league_data = league_response.json()
        league_df = pd.DataFrame(league_data)
        print("League info received!")

    except Exception as e:
        print("Failed to fetch league info:", e)

    # Analyze the data
    try:
        stats_df = add_team_stats(league_df, df) 
        print("Stats collected for each owner!")
    except Exception as e:
        print("Failed to gather stats for each owner:", e)

     # simulate the winners
    try:
        simulate(stats_df)
        print("League winner simulated!")
    except Exception as e:
        print("Failed to simulate league winners")


    # post the results to server
    payload = {
    "timestamp": time.time(),
    "stats": stats_df.to_dict(orient="records"),
    }

    # 2) POST it to the server
    try:
        r = requests.post(URL + "/stats", json=payload)
        r.raise_for_status()
        print("Posted Stats DataFrames successfully:", r.json())
    except Exception as e:
        print("Failed to POST Stats dataframes:", e)

    try:
        notify_with_sound()
    except Exception as e:
        print("Failed to play notification sound:", e)