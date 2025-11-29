import os
import requests
import app.config as cfg

BASE = "https://api.pandascore.co/valorant"

def _safe(s, d="TBD"):
    return s if isinstance(s, str) and s.strip() else d

def team_matches(team_query: str, per_page: int = 5) -> list[dict]:
    url = f"{BASE}/matches"
    params = {"search[opponent_name]": team_query, "per_page": per_page, "sort": "-begin_at"}
    headers = {"Authorization": f"Bearer {cfg.PANDASCORE_API_KEY}"}
    r = requests.get(url, params=params, headers=headers, timeout=20)
    r.raise_for_status()
    out = []
    for m in r.json():
        name = _safe(m.get("name"))
        status = _safe(m.get("status"))
        begin_at = _safe(m.get("begin_at"))
        tournament = (m.get("tournament") or {}).get("name")
        league = (m.get("league") or {}).get("name")
        event = _safe(tournament or league, "Unknown Event")
        opps = m.get("opponents") or []
        names = []
        for o in opps:
            opp = (o or {}).get("opponent") or {}
            names.append(_safe(opp.get("name")))
        teams = ", ".join(names) if names else "TBD vs TBD"
        out.append({"begin_at": begin_at, "status": status, "event": event, "name": name, "teams": teams})
    return out
