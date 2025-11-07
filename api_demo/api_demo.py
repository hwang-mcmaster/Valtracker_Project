import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("PANDASCORE_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing PANDASCORE_API_KEY in .env")

url = "https://api.pandascore.co/valorant/matches"
params = {"page": 1, "per_page": 3, "sort": "-begin_at"}
headers = {"Authorization": f"Bearer {API_KEY}"}

print("Fetching Valorant matches from Pandascore...")
resp = requests.get(url, params=params, headers=headers, timeout=15)
resp.raise_for_status()
data = resp.json()

print(f"Got {len(data)} matches.")
for i in data:
    # Helpers. the initial attempt showing that the result could be none and give error.
    def safe(x, default="TBD"):
        if isinstance(x, str) and x.strip():
            return x
        else:
            return default

    name = safe(i.get("name"))
    status = safe(i.get("status"))
    begin_at = safe(i.get("begin_at"))
    # Some payloads have tournament or league; use whichever exists
    tournament = (i.get("tournament") or {}).get("name")
    league = (i.get("league") or {}).get("name")
    event = safe(tournament or league, "Unknown Event")

    opps = i.get("opponents") or []
    team_names = []
    for o in opps:
        if o:
            opp = o.get("opponent")
        else:
            opp = None

        if not opp:
            opp = {}
        team_names.append(safe(opp.get("name")))

    # In case list is empty
    teams_str = ", ".join(team_names) if team_names else "TBD vs TBD"

    print(f"- {begin_at} | Status: {status} | Event: {event} | {name} | Teams: {teams_str}")
