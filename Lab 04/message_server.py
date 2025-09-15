"""
Message Server for Friend
-------------------------
Listens for incoming messages from friends and echoes them back.
"""
import socket


def main():
    host = '0.0.0.0'  # Listen on all interfaces
    
    try:
        port = int(input("Enter server port (default 8000): ") or "8000")
    except ValueError:
        print("Invalid port number. Exiting.")
        return

    data_payload = 1024  # Max bytes to receive at once

    # Create a TCP socket using context manager for proper cleanup
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable address reuse
        server_address = (host, port)
        
        print(f"🚀 Starting message server on {host}:{port}")
        print("📡 Waiting for messages from friends...")
        print("💡 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        try:
            sock.bind(server_address)
            sock.listen(5)  # Allow up to 5 connections in queue
            
            while True:
                print("⏳ Waiting for connection...")
                client, address = sock.accept()
                
                with client:
                    print(f"✅ Connection from {address[0]}:{address[1]}")
                    
                    # Receive data from client
                    data = client.recv(data_payload)
                    if data:
                        message = data.decode('utf-8')
                        print(f"📥 Received: {message}")
                        
                        # Echo the data back to the client
                        client.sendall(data)
                        print(f"📤 Echoed back to {address[0]}:{address[1]}")
                        print("-" * 30)
                    else:
                        print("❌ No data received from client.")
                        
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            print("🔌 Server shutting down.")


if __name__ == "__main__":
    main()
