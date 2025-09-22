
#!/usr/bin/env python3
import argparse
import socket
from contextlib import closing

def run_server(host: str = "127.0.0.1", port: int = 5000) -> None:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        print(f"Echo server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(65536)
                if data:
                    conn.sendall(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple echo server for Task 03")
    parser.add_argument("--host", default="127.0.0.1", help="Host/interface to bind (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind (default 5000)")
    args = parser.parse_args()
    run_server(args.host, args.port)
