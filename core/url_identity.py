"""URL identity helpers that do not require network access."""

from __future__ import annotations

from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse, urlunparse


def extract_youtube_video_id(source_url: str) -> str | None:
    """Extract a YouTube video identifier from a common video URL.

    Args:
        source_url: Candidate YouTube URL.

    Returns:
        The video identifier when the URL contains one, otherwise ``None``.
    """
    parsed_url = urlparse(source_url.strip())
    host = parsed_url.netloc.lower().removeprefix("www.")
    if host == "youtu.be":
        video_id = parsed_url.path.strip("/").split("/", 1)[0]
        return video_id or None
    if host not in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        return None
    if parsed_url.path.startswith("/shorts/"):
        video_id = parsed_url.path.removeprefix("/shorts/").split("/", 1)[0]
        return video_id or None
    video_values = parse_qs(parsed_url.query).get("v", [])
    return video_values[0].strip() if video_values and video_values[0].strip() else None


def normalize_url_for_comparison(source_url: str) -> str:
    """Normalize a URL for local identity comparisons.

    Args:
        source_url: URL to normalize.

    Returns:
        A stable, fragment-free URL representation.
    """
    parsed_url = urlparse(source_url.strip())
    normalized_query = urlencode(sorted(parse_qsl(parsed_url.query, keep_blank_values=True)))
    normalized_path = parsed_url.path.rstrip("/") or "/"
    return urlunparse(
        (
            parsed_url.scheme.lower(),
            parsed_url.netloc.lower(),
            normalized_path,
            parsed_url.params,
            normalized_query,
            "",
        )
    )
