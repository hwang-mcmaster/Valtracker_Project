from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse, HTMLResponse

from .services.stats_service import recent_for_team
from .services.favorites_service import bootstrap, add, latest
from .services.report_service import team_report_csv
from .adapters.maps_adapter_stub import venue_embed_html

api = FastAPI(
    title="ValTracker API",
    description="Valorant esports stats and favorites backend for 4SA3 project",
    version="1.0.0",
)

bootstrap()


@api.get("/health")
def health():
    return {"ok": True}


@api.get("/team")
def team(name: str = Query(...)):
    matches = recent_for_team(name, 5)
    recent = matches.get("recent") or []
    upcoming = matches.get("upcoming") or []

    if not recent and not upcoming:
        return {
            "team": name,
            "message": "No active team found or no recent match records",
            "matches": {
                "recent": [],
                "upcoming": [],
            },
        }

    return {"team": name, "matches": matches}


@api.post("/favorites")
def mark_favorite(team_name: str = Query(...)):
    new_id = add(team_name)
    return {"id": new_id, "team_name": team_name}


@api.get("/favorites")
def list_favorites():
    return {"favorites": latest(10)}


@api.get("/report.csv", response_class=PlainTextResponse)
def report(team: str = Query(...), n: int = 10):
    return team_report_csv(team, n)


@api.get("/event/map", response_class=HTMLResponse)
def event_map(q: str = Query(..., description="Venue or city text")):
    return venue_embed_html(q)
