#!/usr/bin/env python3
"""
Lab 05 - Task 01: Iterated TCP Server
Tests server with multiple clients using backlog=3 and threading.
"""

import socket
import threading
import time
import argparse
from typing import Optional

class IteratedServer:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.client_counter = 0
        self.running = False
        
    def start_server(self) -> None:
        """Start the TCP server with backlog=3"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.socket.bind((self.host, self.port))
            
            # Set backlog to 3 as required
            self.socket.listen(3)
            
            self.running = True
            print(f"Server started on {self.host}:{self.port}")
            print(f"Backlog set to 3 - waiting for connections...")
            print("Press Ctrl+C to stop the server")
            
            # Accept connections in a loop
            while self.running and self.socket:
                try:
                    # Accept client connection
                    client_socket, client_address = self.socket.accept()
                    print(f"\nNew connection from {client_address}")
                    
                    # Increment client counter for unique identification
                    self.client_counter += 1
                    client_number = self.client_counter
                    
                    # Create and start thread for this client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address, client_number),
                        name=f"Client-{client_number}"
                    )
                    client_thread.daemon = True  # Dies when main thread dies
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
    
    def handle_client(self, client_socket: socket.socket, client_address: tuple, client_number: int) -> None:
        """Handle individual client communication in separate thread"""
        try:
            print(f"Thread started for Client {client_number} from {client_address}")
            
            # Set socket timeout for better responsiveness
            client_socket.settimeout(1.0)
            
            # Send welcome message
            welcome_msg = f"Connected to Client {client_number}"
            client_socket.send(welcome_msg.encode('utf-8'))
            print(f"Sent to Client {client_number}: {welcome_msg}")
            
            # Keep connection alive for communication
            while self.running:
                try:
                    # Receive message from client
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if not message:
                        print(f"Client {client_number} disconnected")
                        break
                    
                    print(f"Received from Client {client_number}: {message}")
                    
                    # Echo back with client number
                    response = f"Server to Client {client_number}: {message}"
                    client_socket.send(response.encode('utf-8'))
                    print(f"Sent to Client {client_number}: {response}")
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error handling Client {client_number}: {e}")
                    break
                    
        except Exception as e:
            print(f"Error in client thread {client_number}: {e}")
        finally:
            # Clean up client connection
            try:
                client_socket.close()
                print(f"Client {client_number} connection closed")
            except:
                pass
    
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
    """Main function to run the server"""
    parser = argparse.ArgumentParser(description='Iterated TCP Server for Lab 05')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
    
    args = parser.parse_args()
    
    # Create and start server
    server = IteratedServer(args.host, args.port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer shutdown complete.")

if __name__ == "__main__":
    main()
