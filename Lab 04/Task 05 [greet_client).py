
#!/usr/bin/env python3
import argparse
import socket

def main() -> None:
    parser = argparse.ArgumentParser(description='Task 05 greeting client')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5050)
    parser.add_argument('message', help='Message to send to server')
    args = parser.parse_args()

    with socket.create_connection((args.host, args.port), timeout=5) as sock:
        sock.sendall(args.message.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR)
        print(sock.recv(4096).decode('utf-8', errors='replace'))

if __name__ == '__main__':
    main()
