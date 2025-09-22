
#!/usr/bin/env python3
import socket
from typing import Tuple

def prompt() -> Tuple[str, int, str]:
    host = input("Server host (default 127.0.0.1): ").strip() or "127.0.0.1"
    port_str = input("Server port (default 5000): ").strip() or "5000"
    try:
        port = int(port_str)
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        raise SystemExit("Invalid port. Use an integer 1-65535.")
    message = input("Message to send: ")
    return host, port, message


def send_message(host: str, port: int, message: str) -> str:
    data = message.encode('utf-8')
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            sock.sendall(data)
            sock.shutdown(socket.SHUT_WR)
            # read response (if echo server), but don't hang forever
            sock.settimeout(5)
            try:
                chunks = []
                while True:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                return b''.join(chunks).decode('utf-8', errors='replace')
            except socket.timeout:
                return ""
    except ConnectionRefusedError:
        raise SystemExit(f"Connection refused: nothing is listening on {host}:{port}. Start a server or use the helper.")
    except socket.timeout:
        raise SystemExit(f"Connection timed out to {host}:{port}. Check host/port and network.")


def main() -> None:
    host, port, message = prompt()
    response = send_message(host, port, message)
    if response:
        print(f"Server responded: {response}")
    else:
        print("Message sent. No response (server may be one-way).")

if __name__ == "__main__":
    main()
