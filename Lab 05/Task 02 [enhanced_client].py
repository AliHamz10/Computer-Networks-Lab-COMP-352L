#!/usr/bin/env python3
"""
Lab 05 - Task 02: Enhanced Client with Continuous Conversation
Prompts for server IP/port and handles continuous conversation with echo.
"""

import socket
import argparse
from typing import Optional

class EnhancedClient:
    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.host = None
        self.port = None
        
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
        """Connect to the server and start conversation"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            print(f"Connecting to {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            
            # Receive connection established message
            connection_msg = self.socket.recv(1024).decode('utf-8')
            print(connection_msg)
            
            # Start continuous conversation
            self.conversation_loop()
            
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure server is running.")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            self.cleanup()
    
    def conversation_loop(self) -> None:
        """Handle continuous conversation with server"""
        print("\nStarting conversation with server...")
        print("Type messages to send to server (or 'disconnect' to exit)")
        print()
        
        try:
            while True:
                # Get user input
                message = input()
                
                if not message.strip():
                    continue
                
                # Send message to server
                self.socket.send(message.encode('utf-8'))
                print(f"[Client] {message}")
                
                # Check for disconnect
                if message.strip().lower() == "disconnect":
                    break
                
                # Receive echo response
                response = self.socket.recv(1024).decode('utf-8')
                print(response)
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except Exception as e:
            print(f"Conversation error: {e}")
    
    def cleanup(self) -> None:
        """Clean up client resources"""
        if self.socket:
            try:
                self.socket.close()
                print("Client socket closed")
            except:
                pass

def main() -> None:
    """Main function to run the enhanced client"""
    parser = argparse.ArgumentParser(description='Enhanced TCP Client for Lab 05 Task 02')
    parser.add_argument('--host', help='Server host (if not provided, will prompt)')
    parser.add_argument('--port', type=int, help='Server port (if not provided, will prompt)')
    
    args = parser.parse_args()
    
    # Create client
    client = EnhancedClient()
    
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
