# nfl_standings.py
# A script to fetch and display NFL team records using the ESPN public API
# Standings endpoint: https://site.api.espn.com/apis/site/v2/sports/football/nfl/standings citeturn2file0

import requests
import pandas as pd

STANDINGS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/standings"

def fetch_nfl_standings():
    """
    Fetches the current NFL standings from the ESPN API and returns a list of team records.
    """
    resp = requests.get(STANDINGS_URL)
    resp.raise_for_status()
    data = resp.json()

    records = []
    # The JSON structure contains 'children' for conferences/divisions
    for conference in data.get('children', []):
        for division in conference.get('groups', []):
            for team_entry in division.get('standings', []):
                team = team_entry.get('team', {})
                team_name = team.get('displayName') or team.get('shortDisplayName')
                stats = team_entry.get('stats', [])
                wins = next((int(s['value']) for s in stats if s.get('name') == 'wins'), 0)
                losses = next((int(s['value']) for s in stats if s.get('name') == 'losses'), 0)
                ties = next((int(s['value']) for s in stats if s.get('name') == 'ties'), 0)
                records.append({
                    'Team': team_name,
                    'Wins': wins,
                    'Losses': losses,
                    'Ties': ties
                })
    return records

def display_standings(records):
    """
    Pretty-prints the standings as a sorted table.
    """
    df = pd.DataFrame(records)
    # Compute win percentage
    df['Win%'] = df['Wins'] / (df['Wins'] + df['Losses'] + df['Ties'])
    # Sort by win percentage, then wins
    df = df.sort_values(by=['Win%', 'Wins'], ascending=[False, False])
    print(df.to_string(index=False))

if __name__ == '__main__':
    try:
        standings = fetch_nfl_standings()
        display_standings(standings)
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
