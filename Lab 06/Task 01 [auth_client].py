#!/usr/bin/env python3
"""
Lab 06 - Task 01: Authentication Client
Supports registration, login, and conversation with the multithreaded server.
"""

import socket
import time
import argparse
from typing import Optional

class AuthClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.username: Optional[str] = None
        self.logged_in = False
        
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
    
    def send_chat(self, message: str) -> str:
        """Send a chat message"""
        if not self.logged_in:
            print("[Client] Please login first")
            return ""
        
        chat_message = f"chat:{message}"
        response = self.send_message(chat_message)
        print(f"[Client] Chat response: {response}")
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

def interactive_client():
    """Interactive client for manual testing"""
    parser = argparse.ArgumentParser(description='Interactive Auth Client for Lab 06')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    client = AuthClient(args.host, args.port)
    
    if not client.connect():
        return
    
    try:
        while True:
            print("\n=== Authentication Client ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                client.register(username, password)
                
            elif choice == "2":
                username = input("Username: ").strip()
                password = input("Password: ").strip()
                if client.login(username, password):
                    # Chat loop
                    print("\n--- Chat Mode ---")
                    print("Type 'logout' to logout, 'exit' to quit")
                    while client.logged_in:
                        message = input(f"[{client.username}] ").strip()
                        if message.lower() == 'logout':
                            client.logout()
                            break
                        elif message.lower() == 'exit':
                            break
                        elif message:
                            client.send_chat(message)
                
            elif choice == "3":
                break
            else:
                print("Invalid option")
                
    except KeyboardInterrupt:
        print("\n[Client] Interrupted by user")
    finally:
        client.disconnect()

if __name__ == "__main__":
    interactive_client()
