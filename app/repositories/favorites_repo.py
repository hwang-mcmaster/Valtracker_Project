from app.db import get_conn


def init() -> None:
    """Create the favorites table if it does not exist."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            create table if not exists favorites (
                id bigserial primary key,
                user_id text not null,
                team_name text not null,
                created_at timestamptz not null default now()
            )
            """
        )
        conn.commit()


def add(user_id: str, team_name: str) -> int:
    """Insert one favorite row and return its new id."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "insert into favorites (user_id, team_name) values (%s, %s) returning id",
            (user_id, team_name),
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return new_id


def latest(limit: int = 10) -> list[dict]:
    """Return the most recent favorites."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            select id, user_id, team_name, created_at
            from favorites
            order by created_at desc
            limit %s
            """,
            (limit,),
        )
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]

    return [dict(zip(cols, r)) for r in rows]
