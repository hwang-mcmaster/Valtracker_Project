from app.repositories import favorites_repo as repo


def bootstrap() -> None:
    """Called once at startup to ensure the table exists."""
    repo.init()


def add(team_name: str, user_id: str) -> int:
    """
    Service wrapper for adding a favorite.

    The API passes both team name and user id.
    """
    return repo.add(user_id, team_name)


def latest(limit: int = 10):
    """Return the most recent favorite records."""
    return repo.latest(limit)
