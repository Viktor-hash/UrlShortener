from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple, Optional
from hashids import Hashids
from .stored_url import StoredURL
from urllib.parse import urlparse

class URLService:
    def __init__(self):
        self.url_store: Dict[str, StoredURL] = {}
        self.url_to_code: Dict[str, str] = {}
        self.hashids = Hashids(min_length=6, salt="votre_sel_unique")
        self.id_counter: int = 1

    def is_valid_url(self, url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme in ("http", "https"), result.netloc])
        except Exception:
            return False

    def create_short_url(self, original_url: str, host_url: str) -> dict:
        if not self.is_valid_url(original_url):
            return {
                "error": "URL invalid",
                "already_exists": False
            }
        if original_url in self.url_to_code:
            short_code = self.url_to_code[original_url]
            return {
                "short_code": short_code,
                "short_url": host_url + short_code,
                "already_exists": True
            }

        short_code = self.hashids.encode(self.id_counter)
        self.id_counter += 1

        self.url_store[short_code] = StoredURL(
            url=original_url,
            visits=0,
            created_at=datetime.now()
        )
        self.url_to_code[original_url] = short_code

        return {
            "short_code": short_code,
            "short_url": host_url + short_code,
            "already_exists": False
        }

    def get_stats(self, short_code: str) -> Optional[StoredURL]:
        stored_url = self.url_store.get(short_code)
        if stored_url:
            return stored_url
        return None

    def increment_visits(self, short_code: str) -> Optional[str]:
        stored_url = self.url_store.get(short_code)
        if stored_url:
            stored_url.visits += 1
            return stored_url.url
        return None

    def reset(self):
        self.url_store.clear()
        self.url_to_code.clear()