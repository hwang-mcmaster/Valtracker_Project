from app.repositories.favorites_repo import add_favorite, latest_favorites, init

def bootstrap():
    init()

def add(user_id: str, team_name: str) -> int:
    return add_favorite(user_id, team_name)

def latest(limit: int = 10):
    return [f.__dict__ for f in latest_favorites(limit)]
