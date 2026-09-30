from io import BytesIO
from pathlib import Path


def as_bytes(value: str | bytes) -> bytes:
    return value if isinstance(value, bytes) else value.encode("utf-8")


def safe_filename(title: str, extension: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in " _-" else "_" for ch in title)
    cleaned = "_".join(cleaned.split())
    return f"{cleaned or 'document'}.{extension.lstrip('.')}"


def stream(value: bytes) -> BytesIO:
    buffer = BytesIO(value)
    buffer.seek(0)
    return buffer
