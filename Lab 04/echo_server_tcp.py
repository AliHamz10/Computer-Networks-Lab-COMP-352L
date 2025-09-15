"""
TCP Echo Server
--------------
Listens for a client connection, receives a message, echoes it back, and terminates.
"""

import socket


def main():
    host = 'localhost'  # Server address
    try:
        port = int(input("Enter server port (default 8000): ") or "8000")  # Prompt for port
    except ValueError:
        print("Invalid port number. Exiting.")
        return
    data_payload = 256  # Max bytes to receive at once

    # Create a TCP socket using context manager for proper cleanup
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable address reuse
        server_address = (host, port)
        print(f"Starting up echo server on {host} port {port}")
        try:
            sock.bind(server_address)
            sock.listen(1)  # Listen for a single connection
            print("Waiting to receive message from client...")
            client, address = sock.accept()
            with client:
                print(f"Connection established with {address}")
                # Receive data from client
                data = client.recv(data_payload)
                if data:
                    print(f"Received: {data.decode('utf-8')}")
                    # Echo the data back to the client
                    client.sendall(data)
                    print(f"Sent {len(data)} bytes back to {address}")
                else:
                    print("No data received from client.")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            print("Server shutting down.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer terminated by user.")
