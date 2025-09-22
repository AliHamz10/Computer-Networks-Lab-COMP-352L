
#!/usr/bin/env python3
import socket
from typing import List, Tuple

# 10 sample domains; can be adjusted
DOMAINS: List[str] = [
    "google.com",
    "facebook.com",
    "youtube.com",
    "wikipedia.org",
    "twitter.com",
    "github.com",
    "amazon.com",
    "microsoft.com",
    "apple.com",
    "cloudflare.com",
]

def resolve_domain(domain: str) -> Tuple[str, str]:
    try:
        ip = socket.gethostbyname(domain)
        return domain, ip
    except socket.gaierror as e:
        return domain, f"resolution_error: {e.errno}"


def main() -> None:
    max_len = max(len(d) for d in DOMAINS + ["Domain"])  # column width
    print(f"{'Domain':<{max_len}}  IP Address")
    print("-" * (max_len + 11))
    for d in DOMAINS:
        domain, ip = resolve_domain(d)
        print(f"{domain:<{max_len}}  {ip}")

if __name__ == "__main__":
    main()
