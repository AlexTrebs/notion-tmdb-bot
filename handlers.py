from config import Settings
from typing import Callable

settings = Settings()

DefHandler = Callable[[dict], dict]

def get_directors(crew: list[dict]) -> list[str]:
  """Extract all crew members with job == 'Director'."""
  return [m["name"] for m in crew if m.get("job") == "Director"]

PROP_HANDLERS: dict[str, DefHandler] = {
  "Poster": lambda info: {
    "rich_text": [
      {
        "type": "text",
        "text": {"content": settings.img_base + info.get("poster_path", "")},
      }
    ]
  },
  "Genre": lambda info: {
    "multi_select": [{"name": g["name"]} for g in info.get("genres", [])]
  },
  "Director": lambda info: {
    "rich_text": [
      {
        "type": "text",
        "text": {"content": ", ".join(get_directors(info["credits"]["crew"]))},
      }
    ]
  },
  "Studio / Distributor": lambda info: {
    "multi_select": [{"name": c["name"]} for c in info.get("production_companies", [])]
  },
  "Type": lambda info: {
    "select": {"name": "Movie" if settings.default_kind == "movie" else "Series"}
  },
}
