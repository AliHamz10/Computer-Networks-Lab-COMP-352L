#!/usr/bin/env python3
"""
Lab 05 - Task 03: Authentication Server with Registration and Login
Supports user registration, login, and credential storage.
"""

import socket
import threading
import time
import argparse
import json
import os
from typing import Optional, Dict, Tuple

class AuthServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.credentials_file = "user_credentials.json"
        self.credentials: Dict[str, str] = {}
        self.load_credentials()
        
    def load_credentials(self) -> None:
        """Load user credentials from file"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    self.credentials = json.load(f)
                print(f"Loaded {len(self.credentials)} user credentials")
            else:
                print("No existing credentials file found, starting fresh")
        except Exception as e:
            print(f"Error loading credentials: {e}")
            self.credentials = {}
    
    def save_credentials(self) -> None:
        """Save user credentials to file"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(self.credentials, f, indent=2)
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def start_server(self) -> None:
        """Start the authentication server"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.socket.bind((self.host, self.port))
            
            # Set backlog to 3
            self.socket.listen(3)
            
            self.running = True
            print(f"Authentication server started on {self.host}:{self.port}")
            print("Waiting for connections...")
            
            # Accept connections in a loop
            while self.running and self.socket:
                try:
                    # Accept client connection
                    client_socket, client_address = self.socket.accept()
                    print(f"New connection from {client_address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        name=f"Client-{client_address[0]}:{client_address[1]}"
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    print("\nShutting down server...")
                    self.running = False
                    break
                except Exception as e:
                    print(f"Error accepting connection: {e}")
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.cleanup()
    
    def handle_client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Handle individual client with authentication"""
        try:
            print(f"Handling client from {client_address}")
            
            # Send welcome message
            welcome_msg = "[Server] Welcome! Would you like to (1) Register or (2) Login?"
            client_socket.send(welcome_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {welcome_msg}")
            
            # Get user choice
            choice = self.receive_message(client_socket, client_address)
            if not choice:
                return
                
            print(f"Received choice from {client_address}: {choice}")
            
            if choice.strip() == "1":
                self.handle_registration(client_socket, client_address)
            elif choice.strip() == "2":
                self.handle_login(client_socket, client_address)
            else:
                error_msg = "[Server] Invalid choice. Please choose 1 or 2."
                client_socket.send(error_msg.encode('utf-8'))
                print(f"Sent to {client_address}: {error_msg}")
                
        except Exception as e:
            print(f"Error in client thread {client_address}: {e}")
        finally:
            # Clean up client connection
            try:
                client_socket.close()
                print(f"Client {client_address} connection closed")
            except:
                pass
    
    def handle_registration(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Handle user registration"""
        try:
            # Get username
            username_msg = "[Server] Username:"
            client_socket.send(username_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {username_msg}")
            
            username = self.receive_message(client_socket, client_address)
            if not username:
                return
                
            print(f"Received username from {client_address}: {username}")
            
            # Check if username already exists
            if username in self.credentials:
                error_msg = "[Server] Username already exists. Please choose another."
                client_socket.send(error_msg.encode('utf-8'))
                print(f"Sent to {client_address}: {error_msg}")
                return
            
            # Get password
            password_msg = "[Server] password"
            client_socket.send(password_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {password_msg}")
            
            password = self.receive_message(client_socket, client_address)
            if not password:
                return
                
            print(f"Received password from {client_address}")
            
            # Get password confirmation
            retype_msg = "[Server] Retype password"
            client_socket.send(retype_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {retype_msg}")
            
            password_confirm = self.receive_message(client_socket, client_address)
            if not password_confirm:
                return
                
            print(f"Received password confirmation from {client_address}")
            
            # Validate passwords match
            if password != password_confirm:
                error_msg = "[Server] Passwords do not match. Registration failed."
                client_socket.send(error_msg.encode('utf-8'))
                print(f"Sent to {client_address}: {error_msg}")
                return
            
            # Register user
            self.credentials[username] = password
            self.save_credentials()
            
            success_msg = f"[Server] User '{username}' registered successfully!"
            client_socket.send(success_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {success_msg}")
            
        except Exception as e:
            print(f"Error in registration for {client_address}: {e}")
    
    def handle_login(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Handle user login with retry logic"""
        try:
            max_attempts = 3
            attempts = 0
            
            while attempts < max_attempts:
                # Get username
                username_msg = "[Server] Username:"
                client_socket.send(username_msg.encode('utf-8'))
                print(f"Sent to {client_address}: {username_msg}")
                
                username = self.receive_message(client_socket, client_address)
                if not username:
                    return
                    
                print(f"Received username from {client_address}: {username}")
                
                # Check if username exists
                if username not in self.credentials:
                    error_msg = "[Server] user unknown. Try again."
                    client_socket.send(error_msg.encode('utf-8'))
                    print(f"Sent to {client_address}: {error_msg}")
                    attempts += 1
                    continue
                
                # Get password
                password_msg = "[Server] Password"
                client_socket.send(password_msg.encode('utf-8'))
                print(f"Sent to {client_address}: {password_msg}")
                
                password = self.receive_message(client_socket, client_address)
                if not password:
                    return
                    
                print(f"Received password from {client_address}")
                
                # Validate password
                if self.credentials[username] == password:
                    success_msg = f"[Server] Welcome {username}!"
                    client_socket.send(success_msg.encode('utf-8'))
                    print(f"Sent to {client_address}: {success_msg}")
                    return
                else:
                    error_msg = "[Server] Password incorrect. Try again"
                    client_socket.send(error_msg.encode('utf-8'))
                    print(f"Sent to {client_address}: {error_msg}")
                    attempts += 1
            
            # Max attempts reached
            error_msg = "[Server] Maximum login attempts reached. Connection terminated."
            client_socket.send(error_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {error_msg}")
            
        except Exception as e:
            print(f"Error in login for {client_address}: {e}")
    
    def receive_message(self, client_socket: socket.socket, client_address: tuple) -> Optional[str]:
        """Receive message from client with error handling"""
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {client_address} disconnected")
                return None
            return message.strip()
        except Exception as e:
            print(f"Error receiving message from {client_address}: {e}")
            return None
    
    def cleanup(self) -> None:
        """Clean up server resources"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
                print("Server socket closed")
            except:
                pass

def main() -> None:
    """Main function to run the authentication server"""
    parser = argparse.ArgumentParser(description='Authentication Server for Lab 05 Task 03')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    # Create and start server
    server = AuthServer(args.host, args.port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer shutdown complete.")

if __name__ == "__main__":
    main()
