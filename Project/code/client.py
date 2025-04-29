import requests
from typing import List, Dict

# Configuration
BASE_URL = "http://<YOUR_PI_IP>:8000"  # Replace with your Raspberry Pi's IP and port if needed

# Sample data: 10 players each with 3 teams
players_data = [
    {"name": f"Player{i+1}", "teams": ["NE", "KC", "BUF"]} for i in range(10)
]

# Alternatively, you can customize teams per player
# players_data = [
#     {"name": "Alice", "teams": ["NE", "DAL", "MIA"]},
#     {"name": "Bob",   "teams": ["GB", "SF", "BAL"]},
#     ... (8 more) ...
# ]


def create_players(players: List[Dict]) -> List[Dict]:
    """
    Sends POST /players for each player in the list and returns the API responses.
    """
    created = []
    for p in players:
        resp = requests.post(
            f"{BASE_URL}/players",
            json={"name": p["name"], "teams": p["teams"]}
        )
        if resp.status_code == 201:
            data = resp.json()
            print(f"Created {data['name']} with ID {data['id']} and teams {data['teams']}")
            created.append(data)
        else:
            print(f"Failed to create {p['name']}: {resp.status_code} {resp.text}")
    return created


def main():
    # Initialize the group of players on the server
    created_players = create_players(players_data)
    print("\nAll players registered.\n")
    for pl in created_players:
        print(pl)

if __name__ == "__main__":
    main()
