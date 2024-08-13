import secrets
from datetime import timedelta, datetime, timezone


def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

def default_expiry_date(days: int = 30) -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=days)

