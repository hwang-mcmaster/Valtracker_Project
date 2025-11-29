from app.adapters.esports_adapter import team_matches


def recent_for_team(team_name: str, n: int = 5):
    return team_matches(team_name, completed_limit=n, upcoming_limit=n)
