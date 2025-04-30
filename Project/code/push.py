import requests, time, random
import pandas as pd
import numpy as np


# === Configuration ===
#URL = "http://192.168.50.1:8000"  # Matches your FastAPI endpoint
#URL = "http://172.20.10.3:8000" # local host for testing

# my wifi at home
URL = "http://192.168.1.16:8000"




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


# === Main execution ===
if __name__ == "__main__":
    try:
        df = update_stats("2024")
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

