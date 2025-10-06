#!/usr/bin/env python3
"""
Lab 06 - Task 01: Test Program for Multiple Clients
Creates multiple clients that simultaneously interact with the server.
Half register new accounts, half login and have conversations.
"""

import socket
import threading
import time
import random
from typing import List, Tuple
# Import AuthClient from the same directory
import importlib.util
import os

# Load the auth client module
spec = importlib.util.spec_from_file_location("auth_client", os.path.join(os.path.dirname(__file__), "Task 01 [auth_client].py"))
auth_client_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auth_client_module)
AuthClient = auth_client_module.AuthClient

class TestClient:
    def __init__(self, client_id: int, host: str = '127.0.0.1', port: int = 8000):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.client = AuthClient(host, port)
        self.success = False
        self.error = None
        
    def run_registration_test(self) -> None:
        """Test client that registers a new account"""
        try:
            print(f"[TEST-{self.client_id}] Starting registration test...")
            
            if not self.client.connect():
                self.error = "Connection failed"
                return
            
            # Generate unique username
            username = f"testuser{self.client_id}_{int(time.time())}"
            password = f"password{self.client_id}"
            
            # Register
            if self.client.register(username, password):
                print(f"[TEST-{self.client_id}] Registration successful: {username}")
                self.success = True
            else:
                self.error = "Registration failed"
                
        except Exception as e:
            self.error = f"Registration test error: {e}"
            print(f"[TEST-{self.client_id}] Error: {e}")
        finally:
            self.client.disconnect()
    
    def run_login_conversation_test(self, username: str, password: str) -> None:
        """Test client that logs in and has a conversation"""
        try:
            print(f"[TEST-{self.client_id}] Starting login/conversation test...")
            
            if not self.client.connect():
                self.error = "Connection failed"
                return
            
            # Login
            if not self.client.login(username, password):
                self.error = "Login failed"
                return
            
            print(f"[TEST-{self.client_id}] Login successful: {username}")
            
            # Have a conversation (3-5 messages)
            conversation_messages = [
                f"Hello from client {self.client_id}!",
                f"How is the server handling multiple clients?",
                f"This is message 3 from client {self.client_id}",
                f"Testing concurrent access from client {self.client_id}",
                f"Final message from client {self.client_id}"
            ]
            
            num_messages = random.randint(3, 5)
            for i in range(num_messages):
                message = conversation_messages[i % len(conversation_messages)]
                self.client.send_chat(message)
                time.sleep(random.uniform(0.5, 1.5))  # Random delay between messages
            
            # Logout
            if self.client.logout():
                print(f"[TEST-{self.client_id}] Logout successful")
                self.success = True
            else:
                self.error = "Logout failed"
                
        except Exception as e:
            self.error = f"Login/conversation test error: {e}"
            print(f"[TEST-{self.client_id}] Error: {e}")
        finally:
            self.client.disconnect()

def create_test_users() -> List[Tuple[str, str]]:
    """Create some test users for login testing"""
    users = []
    # Use the existing testuser that we know exists
    users.append(("testuser", "testpass"))
    # Add a few more with predictable names
    for i in range(4):  # Create 4 more test users
        username = f"existinguser{i+1}"
        password = f"testpass{i+1}"
        users.append((username, password))
    return users

def run_concurrent_test(num_clients: int = 10) -> None:
    """Run concurrent test with multiple clients"""
    print(f"=== Starting Concurrent Test with {num_clients} clients ===")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Create test users first (half will register, half will login)
    test_users = create_test_users()
    
    # Create test clients
    test_clients: List[TestClient] = []
    threads: List[threading.Thread] = []
    
    # Half for registration, half for login/conversation
    half = num_clients // 2
    
    # Create registration test clients
    for i in range(half):
        client = TestClient(i + 1)
        test_clients.append(client)
        thread = threading.Thread(target=client.run_registration_test)
        threads.append(thread)
    
    # Create login/conversation test clients
    for i in range(half, num_clients):
        client = TestClient(i + 1)
        test_clients.append(client)
        # Use existing test user for login
        user_idx = (i - half) % len(test_users)
        username, password = test_users[user_idx]
        thread = threading.Thread(
            target=client.run_login_conversation_test,
            args=(username, password)
        )
        threads.append(thread)
    
    # Start all threads
    print(f"Starting {len(threads)} client threads...")
    start_time = time.time()
    
    for thread in threads:
        thread.start()
        time.sleep(0.1)  # Small delay between starts
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Report results
    print("\n" + "=" * 50)
    print("=== TEST RESULTS ===")
    print(f"Total clients: {num_clients}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Average time per client: {duration/num_clients:.2f} seconds")
    
    successful = sum(1 for client in test_clients if client.success)
    failed = sum(1 for client in test_clients if not client.success)
    
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/num_clients)*100:.1f}%")
    
    # Show errors
    if failed > 0:
        print("\n=== ERRORS ===")
        for i, client in enumerate(test_clients):
            if not client.success and client.error:
                print(f"Client {client.client_id}: {client.error}")
    
    print("=" * 50)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Multiple Clients for Lab 06')
    parser.add_argument('--clients', type=int, default=10, help='Number of clients (default: 10)')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    
    args = parser.parse_args()
    
    print("Lab 06 - Task 01: Multiple Client Test")
    print("Make sure the server is running before starting this test!")
    print(f"Server: {args.host}:{args.port}")
    print("Starting test in 3 seconds...")
    time.sleep(3)
    
    run_concurrent_test(args.clients)

if __name__ == "__main__":
    main()
