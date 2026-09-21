import os
import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


def app_data_dir() -> Path:
    """Return the persistent, per-user data directory used by Flet builds."""
    data_dir = Path(os.getenv("FLET_APP_STORAGE_DATA", BASE_DIR))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def local_encryption_key() -> str:
    """Create a stable local key when no key is supplied through the environment."""
    key_file = app_data_dir() / ".bytevault_encryption_key"
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()

    key = secrets.token_urlsafe(32)
    key_file.write_text(key, encoding="utf-8")
    key_file.chmod(0o600)
    return key


class Settings(BaseSettings):
    # Defaults make the installed desktop app work without shipping a .env
    # file or embedding private API credentials in the .deb package.
    DB_URL: str = f"sqlite:///{app_data_dir() / 'bytevault.db'}"
    BYTEVAULT_ENCRYPTION_KEY: str = local_encryption_key()
    BASE_URL: str = "https://api.openai.com/v1"
    API_KEY: str = ""
    
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
