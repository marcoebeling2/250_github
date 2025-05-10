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


# init fastapi app
app = FastAPI()

# team info
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
    "John Taiariol": [Bengals, Colts, Jaguars],
    "Ben Maslowski": [Texans, Cowboys, Saints],
    "Matt Wellener": [Bills, Packers, Giants],
    "Danny Crouse": [Dolphins, Chargers, Commanders],
    "Michael Corrigan": [Chiefs, Bears, Rams],
    "Quintin Wrabley": [Ravens, Buccaneers, Browns],
    "Will Fredrick": [Lions, Steelers, Raiders],
}


df = pd.Series(player_teams).reset_index()
df.columns = ["Owner", "teams"]

# map each owner to a color
owner_color = {
    "Cotter Duffy":    "#4CBB17",
    "Jake Rupert":     "#FAFF56",
    "Seth McKay":      "#CC5140",
    "John Taiariol":  "#E69E39",
    "Ben Maslowski":   "#86A4AD",
    "Matt Wellener":   "#FFFFFF",
    "Danny Crouse":    "#76611D",
    "Michael Corrigan":"#FFC0CB",
    "Quintin Wrabley": "#000000",
    "Will Fredrick":   "#2190CB",
}

font_color = {
    "Cotter Duffy":    "#000000",
    "Jake Rupert":     "#000000",
    "Seth McKay":      "#000000",
    "John Taiariol":  "#000000",
    "Ben Maslowski":   "#000000",
    "Matt Wellener":   "#000000",
    "Danny Crouse":    "#FFFFFF",
    "Michael Corrigan":"#000000",
    "Quintin Wrabley": "#FFFFFF",
    "Will Fredrick":   "#000000",
}

# add the new column (as the third column):
df.insert(2, "color", df["Owner"].map(owner_color))
df.insert(3, "font_color", df["Owner"].map(font_color))


# expected data format
class DataFramePayload(BaseModel):
    timestamp: float
    stats: List[Any]



# routes
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

    # Build card-based data structure

    owner_cards = []
    for idx, row in enumerate(df.to_dict(orient="records")):
        owner_cards.append({
            "owner": row["Owner"],
            "teams": [
                { "name": row.get("team_1","").split(" ")[-1], "wins": row.get("wins_1",0), "losses": row.get("losses_1",0), "pct": row.get("pct_1",0.0) },
                { "name": row.get("team_2","").split(" ")[-1], "wins": row.get("wins_2",0), "losses": row.get("losses_2",0), "pct": row.get("pct_2",0.0) },
                { "name": row.get("team_3","").split(" ")[-1], "wins": row.get("wins_3",0), "losses": row.get("losses_3",0), "pct": row.get("pct_3",0.0) },
                { "name": "Total record", "wins": row.get("total_wins",0), "losses": row.get("total_losses",0), "pct": row.get("total_pct",0.0) },
            ],
            "total_wins":   row.get("total_wins",0),
            "total_losses": row.get("total_losses",0),
            "total_pct":    row.get("total_pct",0.0),
            # 2) pick a color by cycling through the palette
            "color": row.get("color",""),
            "font_color": row.get("font_color",""),
        })

    # Rankings: total wins and win percentage
    ranked_owners = []
    ranked_by_pct = []
    ranked_league_pct = [] 
    if not df.empty:
        ranked_owners_df = df[["Owner", "total_wins"]].copy()
        ranked_owners_df = ranked_owners_df.sort_values(by="total_wins", ascending=False).reset_index(drop=True)
        ranked_owners_df["rank"] = ranked_owners_df.index + 1
        ranked_owners = ranked_owners_df.to_dict(orient="records")

        ranked_pct_df = df[["Owner", "total_pct"]].copy()
        ranked_pct_df = ranked_pct_df.sort_values(by="total_pct", ascending=False).reset_index(drop=True)
        ranked_pct_df["rank"] = ranked_pct_df.index + 1
        ranked_by_pct = ranked_pct_df.to_dict(orient="records")

        ranked_league_df = (
            df[["Owner", "league_win_pct"]]
            .sort_values(by="league_win_pct", ascending=False)
            .reset_index(drop=True)
        )
        ranked_league_df["rank"] = ranked_league_df.index + 1
        ranked_league_pct = ranked_league_df.to_dict(orient="records")

    return templates.TemplateResponse(
        "stats.html",
        {
            "request": request,
            "owner_cards": owner_cards,
            "ranked_owners": ranked_owners,
            "ranked_by_pct": ranked_by_pct,
            "ranked_league_pct": ranked_league_pct,
        }
    )


# redirect to stats_view
@app.get("/")
async def root():
    return RedirectResponse(url="/stats_view")


if __name__ == "__main__":
    import os
    import uvicorn

    
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", 8000))

    uvicorn.run(
        app,
        host=host,
        port=port,
        # reload=True,
    )