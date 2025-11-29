from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse, HTMLResponse
from .services.stats_service import recent_for_team
from .services.favorites_service import bootstrap, add, latest
from .services.report_service import team_report_csv
from .adapters.maps_adapter_stub import venue_embed_html

api = FastAPI(title="ValTracker")

bootstrap()

@api.get("/health")
def health():
    return {"ok": True}

@api.get("/team")
def team(name: str = Query(...)):
    return {"team": name, "matches": recent_for_team(name, 5)}

@api.post("/favorites")
def fav_add(user_id: str = "demo_user", team_name: str = Query(...)):
    rid = add(user_id, team_name)
    return {"id": rid}

@api.get("/favorites")
def fav_latest():
    return {"favorites": latest(10)}

@api.get("/report.csv", response_class=PlainTextResponse)
def report(team: str = Query(...), n: int = 5):
    return team_report_csv(team, n)

@api.get("/event/map", response_class=HTMLResponse)
def event_map(q: str = Query(...)):
    return venue_embed_html(q)
