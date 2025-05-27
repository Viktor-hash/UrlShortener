from dataclasses import dataclass
from datetime import datetime

@dataclass
class StoredURL:
    url: str
    visits: int
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "visits": self.visits,
            "created_at": self.created_at.isoformat()
        }