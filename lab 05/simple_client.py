import socket

def start_client():
    host = input("Enter server IP Address: ")
    port = int(input("Enter server Port: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message = input("Message: ")
    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    print(f"[Server]: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
