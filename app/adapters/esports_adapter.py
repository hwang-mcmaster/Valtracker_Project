import requests
import app.config as cfg

BASE = "https://api.pandascore.co/valorant"

def _safe(s, d="TBD"):
    return s if isinstance(s, str) and s.strip() else d


def _normalize_match(m: dict) -> dict:
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

    return {
        "begin_at": begin_at,
        "status": status,
        "event": event,
        "name": name,
        "teams": teams,
    }


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
    if not isinstance(raw, list):
        print("Unexpected payload from Pandascore", raw)
        return []

    tq = (team_query or "").lower()

    all_normalized = [_normalize_match(m) for m in raw]

    filtered = []
    for row in all_normalized:
        in_name = tq in row["name"].lower()
        in_event = tq in row["event"].lower()
        in_teams = tq in row["teams"].lower()
        if tq and (in_name or in_event or in_teams):
            filtered.append(row)

    if filtered:
        return filtered[:per_page]

    return all_normalized[:per_page]
