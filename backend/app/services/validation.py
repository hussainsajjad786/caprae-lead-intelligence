import re
import unicodedata
from urllib.parse import urlsplit


def normalize_domain(value: str | None) -> str | None:
    if not value or any(c.isspace() for c in value):
        return None
    try:
        parsed = urlsplit(value if '://' in value else 'https://' + value)
        if parsed.scheme not in ('http', 'https') or parsed.username or parsed.password:
            return None
        _ = parsed.port  # Reject invalid ports.
        host = (parsed.hostname or '').rstrip('.').encode('idna').decode('ascii').lower()
        host = host.removeprefix('www.')
        labels = host.split('.')
        if len(host) > 253 or len(labels) < 2 or labels[-1].isdigit():
            return None
        if not all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', x) for x in labels):
            return None
        return host
    except (ValueError, UnicodeError):
        return None


def validate_website(value: str | None) -> bool:
    return normalize_domain(value) is not None


def validate_email(value: str | None) -> bool:
    if not value or len(value) > 254 or value.count('@') != 1:
        return False
    local, domain = value.rsplit('@', 1)
    return bool(
        0 < len(local) <= 64 and not local.startswith('.') and not local.endswith('.')
        and '..' not in local and re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+", local)
        and normalize_domain(domain) == domain.lower().rstrip('.')
        and not domain.endswith('.')
    )


def normalize_company_name(value: str) -> str:
    return ' '.join(re.sub(r'[^\w\s]', ' ', unicodedata.normalize('NFKC', value).casefold()).split())
