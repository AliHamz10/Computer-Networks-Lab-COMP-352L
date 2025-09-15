"""
Message Client to Friend
------------------------
Connects to a friend's IP address, sends a custom message, receives the echoed reply, and closes the connection.
"""
import socket


def main():
    # Get friend's IP address
    friend_ip = input("Enter your friend's IP address: ").strip()
    if not friend_ip:
        print("No IP address provided. Exiting.")
        return
    
    # Get port number
    try:
        port = int(input("Enter server port (default 8000): ") or "8000")
    except ValueError:
        print("Invalid port number. Exiting.")
        return
    
    # Get custom message
    message = input("Enter your message: ").strip()
    if not message:
        message = "Hello from Python client!"
    
    print(f"\nConnecting to {friend_ip}:{port}")
    print(f"Message: {message}")
    print("-" * 50)

    # Use context manager to ensure socket is closed properly
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = (friend_ip, port)
        try:
            sock.connect(server_address)
            print("✅ Connected successfully!")
        except (ConnectionRefusedError, OSError) as e:
            print(f"❌ Connection failed: {e}")
            print("Make sure your friend is running the echo server!")
            return

        try:
            # Send message
            sock.sendall(message.encode('utf-8'))
            print(f"📤 Sent: {message}")
            
            # Receive response
            data = sock.recv(1024)  # Increased buffer size
            response = data.decode('utf-8')
            print(f"📥 Received: {response}")
            
        except Exception as e:
            print(f"❌ Error during communication: {e}")
        finally:
            print("🔌 Closing connection...")
            print("✅ Message sent successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Client terminated by user.")
