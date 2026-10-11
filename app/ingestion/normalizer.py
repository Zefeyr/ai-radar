import hashlib
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# Common tracking parameters to strip
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "fbclid",
    "gclid",
    "_hsenc",
    "_hsmi",
    "mc_cid",
    "mc_eid",
}


def normalize_url(raw_url: str) -> str:
    """
    Cleans a URL by lowercasing scheme/host, stripping tracking queries,
    and removing redundant trailing slashes.
    """
    parsed = urlparse(raw_url.strip())

    # Lowercase protocol and domain
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Normalize path: strip trailing slash unless it is just root '/'
    path = parsed.path
    if path.endswith("/") and len(path) > 1:
        path = path.rstrip("/")

    # Strip marketing/tracking query parameters, sort the rest for consistency
    filtered_queries = [
        (k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in TRACKING_PARAMS
    ]
    filtered_queries.sort(key=lambda x: x[0])
    query = urlencode(filtered_queries)

    # Remove fragment anchors (#heading-1) since content is the same page
    fragment = ""

    return urlunparse((scheme, netloc, path, parsed.params, query, fragment))


def generate_url_hash(url: str) -> str:
    """
    Computes a deterministic SHA-256 hash from a raw URL after normalization.
    Returns a 64-character hexadecimal string.
    """
    cleaned_url = normalize_url(url)
    return hashlib.sha256(cleaned_url.encode("utf-8")).hexdigest()
