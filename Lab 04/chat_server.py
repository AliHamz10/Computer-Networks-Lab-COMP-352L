"""
Two-Way Chat Server
-------------------
Allows multiple clients to connect and chat with each other.
Each message is broadcast to all connected clients.
"""
import socket
import threading
import time

class ChatServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        """Start the chat server"""
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            print(f"🚀 Chat server started on {self.host}:{self.port}")
            print("📡 Waiting for connections...")
            print("💡 Press Ctrl+C to stop the server")
            print("-" * 50)
            
            while True:
                client, address = self.server.accept()
                print(f"✅ New connection from {address[0]}:{address[1]}")
                
                # Start a new thread for each client
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.server.close()
    
    def broadcast(self, message, sender_client=None):
        """Send message to all connected clients except sender"""
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    # Remove client if sending fails
                    self.remove_client(client)
    
    def remove_client(self, client):
        """Remove a client from the chat"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f"👋 {nickname} left the chat!")
            print(f"❌ {nickname} disconnected")
    
    def handle_client(self, client, address):
        """Handle messages from a specific client"""
        try:
            # Get nickname from client
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"📝 {nickname} joined the chat!")
            self.broadcast(f"👋 {nickname} joined the chat!", client)
            
            while True:
                try:
                    message = client.recv(1024).decode('utf-8')
                    if message:
                        print(f"💬 {nickname}: {message}")
                        self.broadcast(f"{nickname}: {message}", client)
                    else:
                        break
                except:
                    break
                    
        except Exception as e:
            print(f"❌ Error handling client {address}: {e}")
        finally:
            self.remove_client(client)
            client.close()

def main():
    try:
        port = int(input("Enter server port (default 8000): ") or "8000")
    except ValueError:
        print("Invalid port number. Exiting.")
        return
    
    server = ChatServer(port=port)
    server.start()

if __name__ == "__main__":
    main()
