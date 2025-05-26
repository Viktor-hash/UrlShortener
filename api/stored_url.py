from dataclasses import dataclass
from datetime import datetime

@dataclass
class StoredURL:
    url: str
    visits: int
    created_at: datetime