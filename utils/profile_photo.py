from pathlib import Path
from uuid import uuid4


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PROFILE_PHOTOS_DIR = ASSETS_DIR / "profile_photos"
MAX_PROFILE_PHOTO_SIZE = 5 * 1024 * 1024  # 5 MiB


def _image_extension(image_bytes: bytes) -> str | None:
    """Return an extension only for image formats we explicitly support."""
    if image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if image_bytes.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if image_bytes.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if len(image_bytes) >= 12 and image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "webp"
    return None


def save_profile_photo(user_id: int, image_bytes: bytes) -> str:
    """Validate and atomically save a picked image, returning its asset path."""
    if not image_bytes:
        raise ValueError("The selected image is empty.")
    if len(image_bytes) > MAX_PROFILE_PHOTO_SIZE:
        raise ValueError("Profile photos must be 5 MB or smaller.")

    extension = _image_extension(image_bytes)
    if extension is None:
        raise ValueError("Choose a PNG, JPEG, GIF, or WebP image.")

    PROFILE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"user_{user_id}_{uuid4().hex}.{extension}"
    destination = PROFILE_PHOTOS_DIR / filename
    temporary_file = destination.with_suffix(f".{extension}.tmp")
    temporary_file.write_bytes(image_bytes)
    temporary_file.replace(destination)
    return f"profile_photos/{filename}"


def delete_profile_photo(photo_path: str | None) -> None:
    """Delete an old managed photo without allowing paths outside the asset folder."""
    if not photo_path:
        return
    candidate = (ASSETS_DIR / photo_path).resolve()
    photos_directory = PROFILE_PHOTOS_DIR.resolve()
    if candidate.parent == photos_directory and candidate.is_file():
        candidate.unlink()
