"""
Two-Way Chat Client
-------------------
Connects to a chat server and allows real-time messaging.
"""
import socket
import threading
import sys

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        
    def connect(self):
        """Connect to the chat server"""
        try:
            self.client.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def receive(self):
        """Receive messages from server"""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("❌ Connection lost!")
                self.client.close()
                break
    
    def write(self):
        """Send messages to server"""
        while True:
            try:
                message = input()
                if message.lower() == '/quit':
                    self.client.close()
                    break
                self.client.send(message.encode('utf-8'))
            except:
                break
    
    def start(self):
        """Start the chat client"""
        if not self.connect():
            return
            
        print("✅ Connected to chat server!")
        print("💡 Type '/quit' to exit")
        print("-" * 50)
        
        # Start threads for receiving and sending
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()
        
        write_thread = threading.Thread(target=self.write)
        write_thread.daemon = True
        write_thread.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            self.client.close()

def main():
    print("💬 Two-Way Chat Client")
    print("=" * 30)
    
    # Get connection details
    host = input("Enter server IP (default localhost): ").strip() or "localhost"
    try:
        port = int(input("Enter server port (default 8000): ") or "8000")
    except ValueError:
        print("Invalid port number. Exiting.")
        return
    
    # Get nickname
    nickname = input("Enter your nickname: ").strip()
    if not nickname:
        nickname = "Anonymous"
    
    # Create and start client
    client = ChatClient(host, port)
    client.nickname = nickname
    client.start()

if __name__ == "__main__":
    import time
    main()
