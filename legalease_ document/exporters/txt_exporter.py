from exporters.common import as_bytes, stream


def export_txt(title: str, content: str):
    payload = f"{title}\n\n{content}".encode("utf-8")
    return stream(payload)
