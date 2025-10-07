#!/usr/bin/env python3
"""
Lab 06 - Task 04: Group Chat Client
Supports registration, login, and group chat functionality with broadcast messages.
"""

import socket
import time
import argparse
from typing import Optional

class GroupChatClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.username: Optional[str] = None
        self.logged_in = False
        self.in_chat_room = False
        
    def connect(self) -> bool:
        """Connect to the server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"[Client] Connected to {self.host}:{self.port}")
            
            # Receive welcome message from server
            welcome = self.socket.recv(1024).decode('utf-8')
            print(f"[Client] Server welcome: {welcome}")
            return True
        except Exception as e:
            print(f"[Client] Connection failed: {e}")
            return False
    
    def send_message(self, message: str) -> str:
        """Send message to server and return response"""
        try:
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            print(f"[Client] Communication error: {e}")
            return ""
    
    def register(self, username: str, password: str) -> bool:
        """Register a new user"""
        message = f"1:{username}:{password}"
        response = self.send_message(message)
        print(f"[Client] Registration response: {response}")
        
        if "registered successfully" in response:
            return True
        return False
    
    def login(self, username: str, password: str) -> bool:
        """Login with existing credentials"""
        message = f"2:{username}:{password}"
        response = self.send_message(message)
        print(f"[Client] Login response: {response}")
        
        if "Welcome" in response and "logged in" not in response:
            self.username = username
            self.logged_in = True
            return True
        return False
    
    def join_chat(self) -> bool:
        """Join the group chat room"""
        if not self.logged_in:
            print("[Client] Please login first")
            return False
        
        response = self.send_message("3")
        print(f"[Client] Join chat response: {response}")
        
        if "joined the group chat" in response:
            self.in_chat_room = True
            return True
        return False
    
    def send_broadcast(self, message: str) -> str:
        """Send a broadcast message to all clients in chat room"""
        if not self.in_chat_room:
            print("[Client] Please join chat room first")
            return ""
        
        broadcast_message = f"broadcast:{message}"
        response = self.send_message(broadcast_message)
        print(f"[Client] Broadcast response: {response}")
        return response
    
    def send_private_chat(self, message: str) -> str:
        """Send a private chat message"""
        if not self.logged_in:
            print("[Client] Please login first")
            return ""
        
        chat_message = f"chat:{message}"
        response = self.send_message(chat_message)
        print(f"[Client] Private chat response: {response}")
        return response
    
    def logout(self) -> bool:
        """Logout from the server"""
        if not self.logged_in:
            print("[Client] Not logged in")
            return False
        
        response = self.send_message("logout")
        print(f"[Client] Logout response: {response}")
        
        if "Logged out successfully" in response:
            self.logged_in = False
            self.username = None
            self.in_chat_room = False
            return True
        return False
    
    def disconnect(self) -> None:
        """Disconnect from server"""
        if self.socket:
            try:
                self.socket.close()
                print("[Client] Disconnected from server")
            except:
                pass

def interactive_group_chat_client():
    """Interactive group chat client for manual testing"""
    parser = argparse.ArgumentParser(description='Interactive Group Chat Client for Lab 06')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    client = GroupChatClient(args.host, args.port)
    
    if not client.connect():
        return
    
    try:
        while True:
            print("\n=== Group Chat Client ===")
            print("1. Register")
            print("2. Login")
            print("3. Join Chat Room")
            print("4. Send Broadcast Message")
            print("5. Send Private Message")
            print("6. Logout")
            print("7. Exit")
            choice = input("Choose option (1-7): ").strip()
            
            if choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                client.register(username, password)
                
            elif choice == "2":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                client.login(username, password)
                
            elif choice == "3":
                if client.join_chat():
                    print("\n--- Group Chat Mode ---")
                    print("Type 'broadcast:message' to send to all clients")
                    print("Type 'chat:message' for private message")
                    print("Type 'logout' to logout")
                    while client.in_chat_room and client.logged_in:
                        message = input(f"[{client.username}] ").strip()
                        if message.lower() == 'logout':
                            client.logout()
                            break
                        elif message.lower() == 'exit':
                            break
                        elif message.startswith('broadcast:'):
                            client.send_broadcast(message[10:])
                        elif message.startswith('chat:'):
                            client.send_private_chat(message[5:])
                        elif message:
                            # Default to broadcast if no prefix
                            client.send_broadcast(message)
                
            elif choice == "4":
                if client.in_chat_room:
                    message = input("Broadcast message: ").strip()
                    if message:
                        client.send_broadcast(message)
                else:
                    print("[Client] Please join chat room first")
                
            elif choice == "5":
                if client.logged_in:
                    message = input("Private message: ").strip()
                    if message:
                        client.send_private_chat(message)
                else:
                    print("[Client] Please login first")
                
            elif choice == "6":
                client.logout()
                
            elif choice == "7":
                break
            else:
                print("Invalid option")
                
    except KeyboardInterrupt:
        print("\n[Client] Interrupted by user")
    finally:
        client.disconnect()

if __name__ == "__main__":
    interactive_group_chat_client()
