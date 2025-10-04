#!/usr/bin/env python3
"""
Lab 05 - Task 03: Authentication Client with Registration and Login
Handles user registration and login flow with server.
"""

import socket
import argparse
from typing import Optional

class AuthClient:
    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        
    def get_server_info(self) -> None:
        """Get server IP address and port from user"""
        print("Enter server IP Address: ", end="")
        self.host = input().strip()
        
        print("Enter server port: ", end="")
        try:
            self.port = int(input().strip())
        except ValueError:
            print("Invalid port number. Using default 8000.")
            self.port = 8000
    
    def connect_to_server(self) -> None:
        """Connect to the server and start authentication"""
        if not self.host or not self.port:
            print("Error: Server host and port not set")
            return
            
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            print(f"Connecting to {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            
            # Start authentication process
            self.authentication_flow()
            
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure server is running.")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            self.cleanup()
    
    def authentication_flow(self) -> None:
        """Handle the complete authentication flow"""
        try:
            if not self.socket:
                print("Error: No socket connection")
                return
            
            # Receive welcome message
            welcome_msg = self.receive_message()
            if not welcome_msg:
                return
            print(welcome_msg)
            
            # Get user choice
            print("Enter your choice (1 or 2): ", end="")
            choice = input().strip()
            self.send_message(choice)
            print(f"[Client] {choice}")
            
            if choice == "1":
                self.handle_registration()
            elif choice == "2":
                self.handle_login()
            else:
                print("Invalid choice. Please restart the client.")
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except Exception as e:
            print(f"Authentication error: {e}")
    
    def handle_registration(self) -> None:
        """Handle user registration process"""
        try:
            # Get username
            username_msg = self.receive_message()
            if not username_msg:
                return
            print(username_msg)
            
            print("Enter username: ", end="")
            username = input().strip()
            self.send_message(username)
            print(f"[Client] {username}")
            
            # Get password
            password_msg = self.receive_message()
            if not password_msg:
                return
            print(password_msg)
            
            print("Enter password: ", end="")
            password = input().strip()
            self.send_message(password)
            print(f"[Client] {password}")
            
            # Get password confirmation
            retype_msg = self.receive_message()
            if not retype_msg:
                return
            print(retype_msg)
            
            print("Retype password: ", end="")
            password_confirm = input().strip()
            self.send_message(password_confirm)
            print(f"[Client] {password_confirm}")
            
            # Get registration result
            result_msg = self.receive_message()
            if result_msg:
                print(result_msg)
            
        except Exception as e:
            print(f"Registration error: {e}")
    
    def handle_login(self) -> None:
        """Handle user login process with retry logic"""
        try:
            while True:
                # Get username prompt
                username_msg = self.receive_message()
                if not username_msg:
                    return
                print(username_msg)
                
                print("Enter username: ", end="")
                username = input().strip()
                self.send_message(username)
                print(f"[Client] {username}")
                
                # Get response (could be error or password prompt)
                response = self.receive_message()
                if not response:
                    return
                print(response)
                
                # If it's an error message, continue the loop
                if "user unknown" in response or "Try again" in response:
                    continue
                
                # If it's password prompt, get password
                if "Password" in response:
                    print("Enter password: ", end="")
                    password = input().strip()
                    self.send_message(password)
                    print(f"[Client] {password}")
                    
                    # Get login result
                    result_msg = self.receive_message()
                    if result_msg:
                        print(result_msg)
                        if "Welcome" in result_msg:
                            break  # Successful login
                        elif "Password incorrect" in result_msg:
                            continue  # Try again
                        elif "Maximum login attempts" in result_msg:
                            break  # Max attempts reached
                
        except Exception as e:
            print(f"Login error: {e}")
    
    def send_message(self, message: str) -> None:
        """Send message to server"""
        if self.socket:
            self.socket.send(message.encode('utf-8'))
    
    def receive_message(self) -> Optional[str]:
        """Receive message from server"""
        if not self.socket:
            return None
        try:
            message = self.socket.recv(1024).decode('utf-8')
            if not message:
                print("Server disconnected")
                return None
            return message.strip()
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None
    
    def cleanup(self) -> None:
        """Clean up client resources"""
        if self.socket:
            try:
                self.socket.close()
                print("Client socket closed")
            except:
                pass

def main() -> None:
    """Main function to run the authentication client"""
    parser = argparse.ArgumentParser(description='Authentication Client for Lab 05 Task 03')
    parser.add_argument('--host', help='Server host (if not provided, will prompt)')
    parser.add_argument('--port', type=int, help='Server port (if not provided, will prompt)')
    
    args = parser.parse_args()
    
    # Create client
    client = AuthClient()
    
    # Get server info (use args if provided, otherwise prompt)
    if args.host and args.port:
        client.host = args.host
        client.port = args.port
        print(f"Using server: {client.host}:{client.port}")
    else:
        client.get_server_info()
    
    try:
        client.connect_to_server()
    except KeyboardInterrupt:
        print("\nClient shutdown complete.")

if __name__ == "__main__":
    main()
