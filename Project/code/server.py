import os
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, List
from pyngrok import ngrok, conf
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


# =============================
# Initialize FastAPI app
# =============================
app = FastAPI()

# =============================
# Data: Team assignments
# =============================
Eagles = "Philadelphia Eagles"
Cardinals = "Arizona Cardinals"
Panthers = "Carolina Panthers"
Bengals = "Cincinnati Bengals"
Colts = "Indianapolis Colts"
Jaguars = "Jacksonville Jaguars"
Dolphins = "Miami Dolphins"
Chargers = "Los Angeles Chargers"
Commanders = "Washington Commanders"
Niners = "San Francisco 49ers"
Vikings = "Minnesota Vikings"
Titans = "Tennessee Titans"
Texans = "Houston Texans"
Cowboys = "Dallas Cowboys"
Saints = "New Orleans Saints"
Chiefs = "Kansas City Chiefs"
Bears = "Chicago Bears"
Rams = "Los Angeles Rams"
Lions = "Detroit Lions"
Steelers = "Pittsburgh Steelers"
Raiders = "Las Vegas Raiders"
Jets = "New York Jets"
Falcons = "Atlanta Falcons"
Seahawks = "Seattle Seahawks"
Bills = "Buffalo Bills"
Packers = "Green Bay Packers"
Giants = "New York Giants"
Ravens = "Baltimore Ravens"
Buccaneers = "Tampa Bay Buccaneers"
Broncos = "Denver Broncos"
Patriots = "New England Patriots"
Browns = "Cleveland Browns"


player_teams = {
    "Cotter Duffy": [Eagles, Cardinals, Panthers],
    "Jake Rupert": [Niners, Vikings, Titans],
    "Seth McKay": [Jets, Falcons, Seahawks],
    "John Taiarioli": [Bengals, Colts, Jaguars],
    "Ben Masiowski": [Texans, Cowboys, Saints],
    "Matt Wellener": [Bills, Packers, Giants],
    "Danny Crouse": [Dolphins, Chargers, Commanders],
    "Michael Corrigan": [Chiefs, Bears, Rams],
    "Quintin Wrabley": [Ravens, Buccaneers, Browns],
    "Will Fredrick": [Lions, Steelers, Raiders],
}


# =============================
# DataFrame: player/team pairs
# =============================
df = pd.Series(player_teams).reset_index()
df.columns = ["Owner", "teams"]

# map each owner to a color
owner_colors = {
    "Cotter Duffy":    "#3A8FB7",
    "Jake Rupert":     "#E76F51",
    "Seth McKay":      "#2A9D8F",
    "John Taiarioli":  "#F4A261",
    "Ben Masiowski":   "#264653",
    "Matt Wellener":   "#8ECAE6",
    "Danny Crouse":    "#E9C46A",
    "Michael Corrigan":"#006D77",
    "Quintin Wrabley": "#FFB4A2",
    "Will Fredrick":   "#8338EC",
}

# add the new column (as the third column):
df.insert(2, "color", df["Owner"].map(owner_colors))


# class for getting data from the client rpi
# 1. Define the expected structure of incoming data
class DataFramePayload(BaseModel):
    timestamp: float
    stats: List[Any]



# =============================
# Routes
# =============================
@app.get("/league_info")
async def get_league_info():
    return df.to_dict(orient="records")



@app.post("/stats")
async def receive_dataframes(payload: DataFramePayload):
    # updates the stats
    global latest_stats
    latest_stats = payload.stats  
    print("Timestamp:", payload.timestamp)
    print("Stats:", payload.stats)

    return {"status": "ok", "received_rows_df1": len(payload.stats)}




latest_stats: List[Any] = []
templates = Jinja2Templates(directory="templates")
templates.env.auto_reload = True
templates.env.cache = {}
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/stats_view")
async def stats_view(request: Request):
    df = pd.DataFrame(latest_stats)

    # Visualization: Total wins per owner
    fig, ax = plt.subplots(figsize=(8, 4))
    if not df.empty:
        df.set_index("Owner")["total_wins"].sort_values().plot.barh(ax=ax)
        ax.set_xlabel("Total Wins")
        ax.set_title("League Total Wins by Owner")
        plt.tight_layout()

        os.makedirs("static/graphs", exist_ok=True)
        img_path = "static/graphs/total_wins.png"
        fig.savefig(img_path)
        plt.close(fig)
        plot_url = "/static/graphs/total_wins.png"
    else:
        plot_url = None

    # Build card-based data structure

    owner_cards = []
    for idx, row in enumerate(df.to_dict(orient="records")):
        owner_cards.append({
            "owner": row["Owner"],
            "teams": [
                { "name": row.get("team_1",""), "wins": row.get("wins_1",0), "losses": row.get("losses_1",0), "pct": row.get("pct_1",0.0), "sb_pct": row.get("sb_pct_1","") },
                { "name": row.get("team_2",""), "wins": row.get("wins_2",0), "losses": row.get("losses_2",0), "pct": row.get("pct_2",0.0), "sb_pct": row.get("sb_pct_2","") },
                { "name": row.get("team_3",""), "wins": row.get("wins_3",0), "losses": row.get("losses_3",0), "pct": row.get("pct_3",0.0), "sb_pct": row.get("sb_pct_3","") },
            ],
            "total_wins":   row.get("total_wins",0),
            "total_losses": row.get("total_losses",0),
            "total_pct":    row.get("total_pct",0.0),
            # 2) pick a color by cycling through the palette
            "color": row.get("color","")
        })

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "owner_cards": owner_cards,
            "plot_url": plot_url,
        }
    )


# redirect to stats_view
@app.get("/")
async def root():
    return RedirectResponse(url="/stats_view")



# =============================
# Entry point (dev mode)
# =============================
if __name__ == "__main__":
    # set up ngrok
    conf.get_default().auth_token = "2wRBYTeFGmI0h1kRDtnTzd5Yfmq_5ShVWSkYvfc2b6uBkPv76"
    tunnel = ngrok.connect(8000, bind_tls=True)
    print(f" * ngrok tunnel \"{tunnel.public_url}\" → localhost:8000")

    # 3) Run this exact `app` instance
    import os
    import uvicorn

    # Read host/port from env (if set), otherwise bind to 0.0.0.0:8000
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))

    uvicorn.run(
        app,
        host=host,
        port=port,
        # reload=True,  # only for development
    )