#!/usr/bin/env python3
"""
Lab 06 - Task 03: Multithreaded Server with Client Tracking
Supports multiple concurrent clients with client tracking and management.
"""

import socket
import threading
import time
import argparse
import json
import os
import sys
from typing import Optional, Dict, Set, List
from datetime import datetime

class MultithreadedAuthServerWithClientTracking:
    def __init__(self, host: str = '127.0.0.1', port: int = 8000):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.credentials_file = "user_credentials.json"
        self.credentials: Dict[str, str] = {}
        self.logged_in_users: Set[str] = set()
        self.client_counter = 0
        self.lock = threading.Lock()
        self.active_threads: List[threading.Thread] = []
        self.shutdown_event = threading.Event()
        
        # Client tracking - Task 03 requirements
        self.connected_clients: Dict[int, socket.socket] = {}  # {client_id: socket}
        self.client_info: Dict[int, Dict] = {}  # {client_id: {username, address, connected_time}}
        
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
        """Start the multithreaded authentication server with client tracking"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.socket.bind((self.host, self.port))
            
            # Listen for connections
            self.socket.listen(5)
            
            self.running = True
            print(f"=== Multithreaded Auth Server with Client Tracking ===")
            print(f"Host: {self.host}")
            print(f"Port: {self.port}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("Waiting for connections...")
            print("Commands: 'exit' to shutdown, 'list' to show connected clients")
            print("=" * 60)
            
            # Start shutdown monitoring thread
            shutdown_thread = threading.Thread(target=self.monitor_commands, daemon=True)
            shutdown_thread.start()
            
            # Start client count display thread
            display_thread = threading.Thread(target=self.display_client_count, daemon=True)
            display_thread.start()
            
            # Accept connections in a loop
            while self.running and self.socket:
                try:
                    # Accept client connection
                    client_socket, client_address = self.socket.accept()
                    print(f"\n[CONNECTION] New client from {client_address}")
                    
                    # Increment client counter for unique identification
                    with self.lock:
                        self.client_counter += 1
                        client_number = self.client_counter
                    
                    # Track connected client - Task 03 requirement
                    with self.lock:
                        self.connected_clients[client_number] = client_socket
                        self.client_info[client_number] = {
                            'username': None,
                            'address': client_address,
                            'connected_time': datetime.now(),
                            'logged_in': False
                        }
                    
                    print(f"[CLIENT-{client_number}] Added to client tracking")
                    self.display_client_count_now()
                    
                    # Create and start thread for this client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address, client_number),
                        name=f"Client-{client_number}"
                    )
                    client_thread.daemon = True
                    
                    # Track active threads
                    with self.lock:
                        self.active_threads.append(client_thread)
                    
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    print("\n[SHUTDOWN] Keyboard interrupt received...")
                    self.shutdown_server()
                    break
                except Exception as e:
                    if self.running:
                        print(f"[ERROR] Error accepting connection: {e}")
                    break
                    
        except Exception as e:
            print(f"[ERROR] Server error: {e}")
        finally:
            self.cleanup()
    
    def monitor_commands(self) -> None:
        """Monitor for server commands from console input"""
        try:
            while self.running:
                try:
                    user_input = input().strip().lower()
                    if user_input == 'exit':
                        print("\n[SHUTDOWN] Exit command received...")
                        self.shutdown_server()
                        break
                    elif user_input == 'list':
                        self.list_connected_clients()
                    elif user_input == 'count':
                        self.display_client_count_now()
                    else:
                        print(f"[SERVER] Unknown command: '{user_input}'. Available: exit, list, count")
                except EOFError:
                    # Handle case when input is redirected
                    break
                except KeyboardInterrupt:
                    break
        except Exception as e:
            print(f"[ERROR] Command monitor error: {e}")
    
    def display_client_count(self) -> None:
        """Display client count every 30 seconds"""
        try:
            while self.running and not self.shutdown_event.is_set():
                time.sleep(30)
                if self.running:
                    self.display_client_count_now()
        except Exception as e:
            print(f"[ERROR] Display thread error: {e}")
    
    def display_client_count_now(self) -> None:
        """Display current client count immediately"""
        with self.lock:
            active_count = len(self.connected_clients)
            logged_in_count = sum(1 for info in self.client_info.values() if info['logged_in'])
        
        print(f"\n[CLIENT-COUNT] Active clients: {active_count} | Logged in: {logged_in_count}")
    
    def list_connected_clients(self) -> None:
        """List all connected clients - Task 03 requirement"""
        with self.lock:
            if not self.connected_clients:
                print("\n[CLIENT-LIST] No clients currently connected")
                return
            
            print(f"\n[CLIENT-LIST] Connected clients ({len(self.connected_clients)}):")
            print("-" * 80)
            print(f"{'ID':<6} {'Username':<15} {'Address':<20} {'Status':<12} {'Connected':<20}")
            print("-" * 80)
            
            for client_id, info in self.client_info.items():
                username = info['username'] or 'Not logged in'
                address = f"{info['address'][0]}:{info['address'][1]}"
                status = "Logged in" if info['logged_in'] else "Connected"
                connected_time = info['connected_time'].strftime('%H:%M:%S')
                
                print(f"{client_id:<6} {username:<15} {address:<20} {status:<12} {connected_time:<20}")
            
            print("-" * 80)
    
    def shutdown_server(self) -> None:
        """Gracefully shutdown the server"""
        print("\n[SHUTDOWN] Initiating graceful server shutdown...")
        self.running = False
        self.shutdown_event.set()
        
        # Close the main socket to stop accepting new connections
        if self.socket:
            try:
                self.socket.close()
                print("[SHUTDOWN] Main socket closed")
            except:
                pass
        
        # Close all client connections
        with self.lock:
            for client_id, client_socket in self.connected_clients.items():
                try:
                    client_socket.close()
                    print(f"[SHUTDOWN] Closed connection for client {client_id}")
                except:
                    pass
            self.connected_clients.clear()
            self.client_info.clear()
        
        # Wait for all active threads to complete
        print(f"[SHUTDOWN] Waiting for {len(self.active_threads)} active threads to complete...")
        
        for thread in self.active_threads[:]:  # Create a copy to avoid modification during iteration
            if thread.is_alive():
                print(f"[SHUTDOWN] Waiting for thread {thread.name} to complete...")
                thread.join(timeout=5.0)  # Wait up to 5 seconds per thread
                if thread.is_alive():
                    print(f"[WARNING] Thread {thread.name} did not complete within timeout")
        
        print("[SHUTDOWN] All threads have been processed")
        print("[SHUTDOWN] Server shutdown complete")
    
    def handle_client(self, client_socket: socket.socket, client_address: tuple, client_number: int) -> None:
        """Handle individual client communication in separate thread"""
        username = None
        try:
            print(f"[CLIENT-{client_number}] Thread started from {client_address}")
            
            # Set socket timeout for better responsiveness
            client_socket.settimeout(1.0)
            
            # Send welcome message
            welcome_msg = f"[Server] Welcome! Choose an option:\n1. Register\n2. Login\n3. Exit"
            client_socket.send(welcome_msg.encode('utf-8'))
            
            # Handle client requests
            while self.running and not self.shutdown_event.is_set():
                try:
                    # Receive message from client
                    message = client_socket.recv(1024).decode('utf-8').strip()
                    
                    if not message:
                        print(f"[CLIENT-{client_number}] Disconnected")
                        break
                    
                    print(f"[CLIENT-{client_number}] Received: {message}")
                    
                    # Process client request
                    response = self.process_request(message, client_number, username)
                    
                    if response:
                        client_socket.send(response.encode('utf-8'))
                        print(f"[CLIENT-{client_number}] Sent: {response}")
                    
                    # Update username if login was successful
                    if message.startswith("2:") and "Welcome" in response:
                        # Extract just the username (before the second colon)
                        parts = message[2:].strip().split(":", 1)
                        if len(parts) >= 1:
                            username = parts[0].strip()
                            # Update client info
                            with self.lock:
                                if client_number in self.client_info:
                                    self.client_info[client_number]['username'] = username
                                    self.client_info[client_number]['logged_in'] = True
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[CLIENT-{client_number}] Error: {e}")
                    break
                    
        except Exception as e:
            print(f"[CLIENT-{client_number}] Thread error: {e}")
        finally:
            # Clean up client connection
            if username and username in self.logged_in_users:
                with self.lock:
                    self.logged_in_users.discard(username)
                print(f"[CLIENT-{client_number}] User '{username}' logged out")
            
            # Remove from client tracking
            with self.lock:
                if client_number in self.connected_clients:
                    del self.connected_clients[client_number]
                if client_number in self.client_info:
                    del self.client_info[client_number]
                print(f"[CLIENT-{client_number}] Removed from client tracking")
            
            try:
                client_socket.close()
                print(f"[CLIENT-{client_number}] Connection closed")
            except:
                pass
            
            # Remove this thread from active threads list
            with self.lock:
                if threading.current_thread() in self.active_threads:
                    self.active_threads.remove(threading.current_thread())
            
            # Display updated client count
            self.display_client_count_now()
    
    def process_request(self, message: str, client_number: int, username: Optional[str]) -> str:
        """Process client request and return response"""
        try:
            if message.startswith("1:"):  # Registration
                return self.handle_registration(message[2:].strip(), client_number)
            elif message.startswith("2:"):  # Login
                return self.handle_login(message[2:].strip(), client_number)
            elif message.startswith("3"):  # Exit
                return "[Server] Goodbye!"
            elif message.startswith("chat:"):  # Chat message
                return self.handle_chat(message[5:].strip(), username, client_number)
            elif message.startswith("logout"):  # Logout
                return self.handle_logout(username, client_number)
            else:
                return "[Server] Invalid option. Use 1 (Register), 2 (Login), 3 (Exit), or chat:message"
        except Exception as e:
            return f"[Server] Error processing request: {e}"
    
    def handle_registration(self, credentials: str, client_number: int) -> str:
        """Handle user registration"""
        try:
            parts = credentials.split(":", 1)
            if len(parts) != 2:
                return "[Server] Invalid format. Use: username:password"
            
            username, password = parts[0].strip(), parts[1].strip()
            
            if not username or not password:
                return "[Server] Username and password cannot be empty"
            
            with self.lock:
                if username in self.credentials:
                    return f"[Server] Username '{username}' already exists. Please choose another."
                
                # Register new user
                self.credentials[username] = password
                self.save_credentials()
            
            print(f"[CLIENT-{client_number}] User '{username}' registered successfully")
            return f"[Server] User '{username}' registered successfully!"
            
        except Exception as e:
            return f"[Server] Registration error: {e}"
    
    def handle_login(self, credentials: str, client_number: int) -> str:
        """Handle user login"""
        try:
            parts = credentials.split(":", 1)
            if len(parts) != 2:
                return "[Server] Invalid format. Use: username:password"
            
            username, password = parts[0].strip(), parts[1].strip()
            
            with self.lock:
                if username not in self.credentials:
                    return "[Server] User unknown. Try again."
                
                if self.credentials[username] != password:
                    return "[Server] Password incorrect. Try again."
                
                if username in self.logged_in_users:
                    return "[Server] User already logged in from another session."
                
                # Login successful
                self.logged_in_users.add(username)
            
            print(f"[CLIENT-{client_number}] User '{username}' logged in successfully")
            return f"[Server] Welcome {username}! You can now chat. Use 'chat:message' to send messages or 'logout' to logout."
            
        except Exception as e:
            return f"[Server] Login error: {e}"
    
    def handle_chat(self, message: str, username: Optional[str], client_number: int) -> str:
        """Handle chat messages"""
        if not username:
            return "[Server] Please login first to chat."
        
        if not message:
            return "[Server] Message cannot be empty."
        
        print(f"[CLIENT-{client_number}] {username} says: {message}")
        return f"[Server] {username}: {message}"
    
    def handle_logout(self, username: Optional[str], client_number: int) -> str:
        """Handle user logout"""
        if not username:
            return "[Server] You are not logged in."
        
        with self.lock:
            self.logged_in_users.discard(username)
            # Update client info
            if client_number in self.client_info:
                self.client_info[client_number]['logged_in'] = False
        
        print(f"[CLIENT-{client_number}] User '{username}' logged out")
        return "[Server] Logged out successfully. Goodbye!"
    
    def cleanup(self) -> None:
        """Clean up server resources"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
                print("[SERVER] Server socket closed")
            except:
                pass

def main() -> None:
    """Main function to run the server"""
    parser = argparse.ArgumentParser(description='Multithreaded Auth Server with Client Tracking for Lab 06')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    # Create and start server
    server = MultithreadedAuthServerWithClientTracking(args.host, args.port)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server shutdown complete.")

if __name__ == "__main__":
    main()
