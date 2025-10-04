#!/usr/bin/env python3
"""
Lab 05 - Task 02: Enhanced Server with Continuous Conversation
Supports connection established message and echo functionality with disconnect handling.
"""

import socket
import threading
import time
import argparse
from typing import Optional

class EnhancedServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        
    def start_server(self) -> None:
        """Start the enhanced TCP server with echo functionality"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.socket.bind((self.host, self.port))
            
            # Set backlog to 3 as required
            self.socket.listen(3)
            
            self.running = True
            print(f"Listening on {self.host}:{self.port}")
            
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
        """Handle individual client with echo functionality"""
        try:
            print(f"Handling client from {client_address}")
            
            # Send connection established message immediately
            connection_msg = "[Server]Connection Established."
            client_socket.send(connection_msg.encode('utf-8'))
            print(f"Sent to {client_address}: {connection_msg}")
            
            # Continuous conversation loop
            while self.running:
                try:
                    # Receive message from client
                    message = client_socket.recv(1024).decode('utf-8')
                    
                    if not message:
                        print(f"Client {client_address} disconnected")
                        break
                    
                    print(f"Received from {client_address}: {message}")
                    
                    # Check for disconnect message
                    if message.strip().lower() == "disconnect":
                        disconnect_msg = "[Server]Connection terminated."
                        client_socket.send(disconnect_msg.encode('utf-8'))
                        print(f"Sent to {client_address}: {disconnect_msg}")
                        print(f"Listening on {self.host}:{self.port}")
                        break
                    
                    # Echo back with (Echoed) suffix
                    echo_msg = f"[Server] {message} (Echoed)"
                    client_socket.send(echo_msg.encode('utf-8'))
                    print(f"Sent to {client_address}: {echo_msg}")
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error handling client {client_address}: {e}")
                    break
                    
        except Exception as e:
            print(f"Error in client thread {client_address}: {e}")
        finally:
            # Clean up client connection
            try:
                client_socket.close()
                print(f"Client {client_address} connection closed")
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
    """Main function to run the enhanced server"""
    parser = argparse.ArgumentParser(description='Enhanced TCP Server for Lab 05 Task 02')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    # Create and start server
    server = EnhancedServer(args.host, args.port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nServer shutdown complete.")

if __name__ == "__main__":
    main()
