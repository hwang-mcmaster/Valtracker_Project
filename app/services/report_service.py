import io
import csv
from app.adapters.esports_adapter import team_matches

def team_report_csv(team_name: str, n: int = 5) -> str:
    rows = team_matches(team_name, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["begin_at","status","event","name","teams"])
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()
