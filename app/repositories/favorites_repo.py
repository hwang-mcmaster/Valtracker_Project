from app.db import get_conn
from app.models import Favorite

DDL = """
CREATE TABLE IF NOT EXISTS favorites(
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(64),
  team_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
"""

def init():
    with get_conn() as c, c.cursor() as cur:
        cur.execute(DDL)

def add_favorite(user_id: str, team_name: str) -> int:
    with get_conn() as c, c.cursor() as cur:
        cur.execute("INSERT INTO favorites(user_id,team_name) VALUES(%s,%s) RETURNING id", (user_id, team_name))
        return cur.fetchone()[0]

def latest_favorites(limit: int = 10) -> list[Favorite]:
    with get_conn() as c, c.cursor() as cur:
        cur.execute("SELECT id,user_id,team_name FROM favorites ORDER BY id DESC LIMIT %s", (limit,))
        rows = cur.fetchall()
        return [Favorite(id=r[0], user_id=r[1], team_name=r[2]) for r in rows]
