"""
TCP Echo Client
---------------
Connects to a TCP echo server, sends a message, receives the echoed reply, and closes the connection.
"""
import socket


def main():
    host = 'localhost'  # Server address (localhost for local testing)
    try:
        port = int(input("Enter server port: "))  # Prompt user for server port
    except ValueError:
        print("Invalid port number. Exiting.")
        return

    message = "Test message. This will be echoed"  # Message to send

    # Use context manager to ensure socket is closed properly
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = (host, port)
        print(f"Connecting to {host} port {port}")
        try:
            sock.connect(server_address)
        except (ConnectionRefusedError, OSError) as e:
            print(f"Connection failed: {e}")
            return

        print(f"Sending: {message}")
        try:
            sock.sendall(message.encode('utf-8'))  # Send message to server
            data = sock.recv(256)  # Receive response (up to 256 bytes)
            print(f"Received: {data.decode('utf-8')}")  # Print decoded response
        except Exception as e:
            print(f"Error during communication: {e}")
        finally:
            print("Closing connection to the server.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nClient terminated by user.")
