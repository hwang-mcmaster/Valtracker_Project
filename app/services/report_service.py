import io
import csv
from app.adapters.esports_adapter import flat_matches


def team_report_csv(team_name: str, n: int = 10) -> str:
    per_section = n or 10

    primary = flat_matches(team_name, limit=40, include_canceled=True)
    fallback = flat_matches("", limit=40, include_canceled=True)

    all_rows: list[dict] = []
    seen = set()

    def add_rows(rows):
        for r in rows:
            key = (r["begin_at"], r["name"], r["teams"])
            if key in seen:
                continue
            seen.add(key)
            all_rows.append(
                {
                    "bucket": "",
                    "begin_at": r["begin_at"],
                    "status": r["status"],
                    "event": r["event"],
                    "name": r["name"],
                    "teams": r["teams"],
                }
            )

    add_rows(primary)
    add_rows(fallback)

    finished = [r for r in all_rows if (r["status"] or "").lower() == "finished"]
    others = [r for r in all_rows if (r["status"] or "").lower() != "finished"]

    finished = finished[:per_section]
    others = others[:per_section]

    for r in finished:
        r["bucket"] = "finished"
    for r in others:
        if r["bucket"] == "":
            r["bucket"] = "other"

    ordered = finished + others

    buf = io.StringIO()
    fieldnames = ["bucket", "begin_at", "status", "event", "name", "teams"]
    w = csv.DictWriter(buf, fieldnames=fieldnames)
    w.writeheader()
    for r in ordered:
        w.writerow(r)

    return buf.getvalue()
