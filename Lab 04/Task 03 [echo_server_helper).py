
#!/usr/bin/env python3
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
    run_server()
