import io
import csv
from app.adapters.esports_adapter import team_matches


def team_report_csv(team_name: str, n: int = 5) -> str:
    buckets = team_matches(team_name, completed_limit=n, upcoming_limit=n)

    recent = buckets.get("recent") or []
    upcoming = buckets.get("upcoming") or []

    rows: list[dict] = []
    for r in recent:
        rows.append(
            {
                "bucket": "recent",
                "begin_at": r["begin_at"],
                "status": r["status"],
                "event": r["event"],
                "name": r["name"],
                "teams": r["teams"],
            }
        )
    for r in upcoming:
        rows.append(
            {
                "bucket": "upcoming",
                "begin_at": r["begin_at"],
                "status": r["status"],
                "event": r["event"],
                "name": r["name"],
                "teams": r["teams"],
            }
        )

    buf = io.StringIO()
    fieldnames = ["bucket", "begin_at", "status", "event", "name", "teams"]
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

    return buf.getvalue()
