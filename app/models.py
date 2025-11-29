from dataclasses import dataclass

@dataclass
class Favorite:
    id: int | None
    user_id: str
    team_name: str
