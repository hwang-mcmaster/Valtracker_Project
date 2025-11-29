from ..adapters.esports_adapter import team_matches


def recent_for_team(team_name: str, n: int = 5) -> dict:
    # first try matches that mention this team
    buckets = team_matches(team_name, completed_limit=n, upcoming_limit=n)
    recent = buckets.get("recent") or []
    upcoming = buckets.get("upcoming") or []

    # if nothing at all, fall back to generic recent Valorant matches
    if not recent and not upcoming:
        buckets = team_matches("", completed_limit=n, upcoming_limit=n)

    return buckets
