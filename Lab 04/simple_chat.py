#!/usr/bin/env python3
"""
Simple Chat with Friend
-----------------------
Easy way to chat with your friend using their IP address.
"""
import socket
import threading
import sys
import time

class SimpleChat:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 8000
        self.friend_ip = None
        self.nickname = None
        self.server_socket = None
        self.client_socket = None
        self.is_server = False
        self.is_client = False
        
    def start_server(self):
        """Start as server (host)"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            print(f"🚀 Server started on {self.host}:{self.port}")
            print("📡 Waiting for your friend to connect...")
            print("💡 Press Ctrl+C to stop")
            print("-" * 50)
            
            self.is_server = True
            
            # Accept connection
            self.client_socket, address = self.server_socket.accept()
            print(f"✅ Friend connected from {address[0]}:{address[1]}")
            print("💬 Start chatting! Type 'quit' to exit")
            print("-" * 30)
            
            # Start receiving messages
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Start sending messages
            self.send_messages()
            
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.cleanup()
    
    def start_client(self, friend_ip):
        """Start as client (connect to friend)"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((friend_ip, self.port))
            
            print(f"✅ Connected to {friend_ip}:{self.port}")
            print("💬 Start chatting! Type 'quit' to exit")
            print("-" * 30)
            
            self.is_client = True
            
            # Start receiving messages
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Start sending messages
            self.send_messages()
            
        except KeyboardInterrupt:
            print("\n👋 Disconnected!")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        finally:
            self.cleanup()
    
    def receive_messages(self):
        """Receive messages from friend"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"📥 Friend: {message}")
                else:
                    break
            except:
                break
    
    def send_messages(self):
        """Send messages to friend"""
        while True:
            try:
                message = input()
                if message.lower() == 'quit':
                    break
                self.client_socket.send(message.encode('utf-8'))
                print(f"📤 You: {message}")
            except:
                break
    
    def cleanup(self):
        """Clean up connections"""
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()

def main():
    print("💬 Simple Chat with Friend")
    print("=" * 40)
    
    chat = SimpleChat()
    
    # Get nickname
    chat.nickname = input("Enter your name: ").strip() or "Anonymous"
    
    # Choose mode
    print("\nChoose mode:")
    print("1. Start Server (Host) - Wait for friend to connect")
    print("2. Connect to Friend - Enter friend's IP")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Start server
        chat.start_server()
        
    elif choice == "2":
        # Connect to friend
        friend_ip = input("Enter friend's IP address: ").strip()
        if not friend_ip:
            print("❌ No IP address provided!")
            return
        
        chat.friend_ip = friend_ip
        chat.start_client(friend_ip)
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
