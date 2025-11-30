from ..adapters.esports_adapter import team_matches


def recent_for_team(team_name: str, n: int = 5) -> dict:
    """
    Return recent and upcoming matches for a given team.

    If the team name does not appear in any match, both lists
    will simply be empty. This makes it clear to the user that
    the search term did not match anything.
    """
    return team_matches(team_name, completed_limit=n, upcoming_limit=n)
