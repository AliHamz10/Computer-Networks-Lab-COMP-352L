import socket
import sys

def start_client(client_number):
    host = "127.0.0.1"
    port = 5000

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = f"Client {client_number}"
        print(f"[Client {client_number}] Sending: {message}")
        client_socket.send(message.encode())

        response = client_socket.recv(1024).decode()
        print(f"[Client {client_number}] Server response: {response}")

        client_socket.close()
        
    except ConnectionRefusedError:
        print(f"[Client {client_number}] Connection refused - server may be full or not running")
    except Exception as e:
        print(f"[Client {client_number}] Error: {e}")

if __name__ == "__main__":
    # Get client number from command line argument or prompt
    if len(sys.argv) > 1:
        client_number = sys.argv[1]
    else:
        client_number = input("Enter client number (1-5): ")
    
    start_client(client_number)
