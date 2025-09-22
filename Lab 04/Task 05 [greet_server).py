
#!/usr/bin/env python3
import argparse
import socket
from contextlib import closing


def build_greeting(message: str, username: str) -> str:
    if not username:
        return "Unknown user"
    delimiters = " ,.!?;:\"'\n\r\t"
    tokens = {t.strip(delimiters).lower() for t in message.split()}
    if username.lower() in tokens:
        return f"Hello, {username}!"
    return "Unknown user"


def run_server(host: str, port: int, username: str) -> None:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"Greet server on {host}:{port} (username='{username}')")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(65536)
                message = data.decode('utf-8', errors='replace') if data else ''
                reply = build_greeting(message, username)
                conn.sendall(reply.encode('utf-8'))


def main() -> None:
    parser = argparse.ArgumentParser(description='Task 05 greeting server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('--user', required=True, help='Username to look for in client message')
    args = parser.parse_args()
    run_server(args.host, args.port, args.user)

if __name__ == '__main__':
    main()
