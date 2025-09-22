
#!/usr/bin/env python3
import socket
from typing import Dict, List, Tuple

# Choose 10 representative ports across well-known and registered ranges
PORTS: List[int] = [20, 21, 22, 23, 25, 53, 67, 80, 110, 443]

def get_service_name(port: int, proto: str = "tcp") -> str:
    try:
        return socket.getservbyport(port, proto)
    except OSError:
        return "unknown"


def collect_services(ports: List[int]) -> List[Tuple[int, str, str]]:
    results: List[Tuple[int, str, str]] = []
    for p in ports:
        tcp = get_service_name(p, "tcp")
        udp = get_service_name(p, "udp")
        results.append((p, tcp, udp))
    return results


def main() -> None:
    rows = collect_services(PORTS)
    header = ("Port", "TCP Service", "UDP Service")
    widths = [max(len(str(r[i])) for r in rows + [(header[0], header[1], header[2])]) for i in range(3)]

    print(f"{header[0]:<{widths[0]}}  {header[1]:<{widths[1]}}  {header[2]:<{widths[2]}}")
    print("-" * (sum(widths) + 4))
    for port, tcp, udp in rows:
        print(f"{port:<{widths[0]}}  {tcp:<{widths[1]}}  {udp:<{widths[2]}}")


if __name__ == "__main__":
    main()
