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


def team_matches(
    team_query: str,
    completed_limit: int = 5,
    upcoming_limit: int = 5,
    include_canceled: bool = False,
) -> dict:
    url = f"{BASE}/matches"
    per_page = (completed_limit + upcoming_limit) * 2 or 10
    params = {"page": 1, "per_page": per_page, "sort": "-begin_at"}
    headers = {"Authorization": f"Bearer {cfg.PANDASCORE_API_KEY}"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error talking to Pandascore {e}")
        return {"recent": [], "upcoming": []}

    raw = r.json()
    if not isinstance(raw, list):
        print("Unexpected payload from Pandascore", raw)
        return {"recent": [], "upcoming": []}

    # trim spaces then lower case so an extra space does not break matching
    tq = (team_query or "").strip().lower()

    def matches_team(row: dict) -> bool:
        if not tq:
            return True
        s = f"{row['name']} {row['event']} {row['teams']}".lower()
        return tq in s

    recent: list[dict] = []
    upcoming: list[dict] = []
    canceled: list[dict] = []

    for m in raw:
        row = _normalize_match(m)
        status_raw = (m.get("status") or "").lower()

        if not matches_team(row):
            continue

        if status_raw in {"finished", "running"}:
            recent.append(row)
        elif status_raw in {"not_started", "upcoming", "postponed"}:
            upcoming.append(row)
        elif status_raw == "canceled":
            canceled.append(row)
        else:
            upcoming.append(row)

    recent = recent[:completed_limit]
    upcoming = upcoming[:upcoming_limit]

    if include_canceled:
        target = completed_limit + upcoming_limit
        have = len(recent) + len(upcoming)
        if have < target and canceled:
            need = target - have
            recent.extend(canceled[:need])
    else:
        if not recent and not upcoming and canceled:
            recent = canceled[:completed_limit]

    return {"recent": recent, "upcoming": upcoming}


def flat_matches(
    team_query: str,
    limit: int = 40,
    include_canceled: bool = True,
) -> list[dict]:
    buckets = team_matches(
        team_query,
        completed_limit=limit,
        upcoming_limit=limit,
        include_canceled=include_canceled,
    )
    recent = buckets.get("recent") or []
    upcoming = buckets.get("upcoming") or []
    rows: list[dict] = []
    rows.extend(recent)
    rows.extend(upcoming)
    return rows
