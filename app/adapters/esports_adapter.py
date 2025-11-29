import requests
import app.config as cfg

BASE = "https://api.pandascore.co/valorant"

def _safe(s, d="TBD"):
    return s if isinstance(s, str) and s.strip() else d

def team_matches(team_query: str, per_page: int = 5) -> list[dict]:
    url = f"{BASE}/matches"
    params = {"page": 1, "per_page": per_page, "sort": "-begin_at"}
    headers = {"Authorization": f"Bearer {cfg.PANDASCORE_API_KEY}"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error talking to Pandascore {e}")
        return []

    raw = r.json()
    out: list[dict] = []

    tq = (team_query or "").lower()

    for m in raw:
        name = _safe(m.get("name"))
        status = _safe(m.get("status"))
        begin_at = _safe(m.get("begin_at"))
        tournament = (m.get("tournament") or {}).get("name")
        league = (m.get("league") or {}).get("name")
        event = _safe(tournament or league, "Unknown Event")

        opps = m.get("opponents") or []
        names: list[str] = []
        for o in opps:
            opp = (o or {}).get("opponent") or {}
            names.append(_safe(opp.get("name")))
        teams = ", ".join(names) if names else "TBD vs TBD"

        if tq and tq not in teams.lower() and tq not in name.lower() and tq not in event.lower():
            continue

        out.append(
            {
                "begin_at": begin_at,
                "status": status,
                "event": event,
                "name": name,
                "teams": teams,
            }
        )

    return out
