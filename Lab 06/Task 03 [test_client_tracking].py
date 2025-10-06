#!/usr/bin/env python3
"""
Lab 06 - Task 03: Test Client Tracking Functionality
Tests the server's ability to track connected clients and display the list command.
"""

import socket
import threading
import time
import subprocess
import sys
import os

def test_client_tracking():
    """Test the client tracking functionality"""
    print("=== Testing Client Tracking Functionality ===")
    print("This test will:")
    print("1. Start the server with client tracking")
    print("2. Connect multiple clients")
    print("3. Test the 'list' command")
    print("4. Test the 'count' command")
    print("5. Verify client tracking works correctly")
    print("=" * 60)
    
    # Start server in background
    print("\n[TEST] Starting server with client tracking...")
    server_process = subprocess.Popen([
        sys.executable, 
        "Task 03 [multithreaded_auth_server_with_client_tracking].py", 
        "--port", "8002"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test multiple client connections
        clients = []
        print("[TEST] Connecting multiple clients...")
        
        # Connect 3 clients
        for i in range(3):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 8002))
            
            # Receive welcome message
            welcome = client_socket.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} connected: {welcome[:50]}...")
            
            clients.append(client_socket)
            time.sleep(0.5)  # Small delay between connections
        
        print(f"[TEST] Connected {len(clients)} clients")
        
        # Test registration for each client
        for i, client in enumerate(clients):
            username = f"tracking_user_{i+1}"
            password = f"testpass_{i+1}"
            
            # Register
            client.send(f"1:{username}:{password}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} registration: {response[:50]}...")
            
            # Login
            client.send(f"2:{username}:{password}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} login: {response[:50]}...")
            
            time.sleep(0.5)
        
        print("\n[TEST] All clients registered and logged in")
        print("[TEST] Check server terminal for 'list' and 'count' commands")
        print("[TEST] In server terminal, type:")
        print("  - 'list' to see all connected clients")
        print("  - 'count' to see client count")
        print("  - 'exit' to shutdown")
        
        # Keep clients connected for a while
        print("\n[TEST] Keeping clients connected for 10 seconds...")
        time.sleep(10)
        
        # Disconnect clients one by one
        print("[TEST] Disconnecting clients...")
        for i, client in enumerate(clients):
            client.close()
            print(f"[TEST] Client {i+1} disconnected")
            time.sleep(1)
        
        print("[TEST] All clients disconnected")
        
    except Exception as e:
        print(f"[TEST] Error during test: {e}")
    finally:
        # Clean up
        for client in clients:
            try:
                client.close()
            except:
                pass
        
        if server_process.poll() is None:
            print("\n[TEST] Server is still running. You can test 'list' and 'count' commands manually.")
            print("[TEST] Press Enter to terminate server...")
            input()
            server_process.terminate()
            server_process.wait(timeout=5)
        else:
            print("[TEST] Server has already terminated")
        
        # Get server output
        stdout, stderr = server_process.communicate()
        if stdout:
            print("\n[TEST] Server output:")
            print(stdout)
        if stderr:
            print("\n[TEST] Server errors:")
            print(stderr)

def test_manual_client_tracking():
    """Instructions for manual client tracking testing"""
    print("\n=== Manual Client Tracking Test Instructions ===")
    print("1. Start the server with client tracking:")
    print("   python3 'Task 03 [multithreaded_auth_server_with_client_tracking].py' --port 8000")
    print()
    print("2. In multiple terminals, connect clients:")
    print("   python3 'Task 01 [auth_client].py' --port 8000")
    print()
    print("3. Register and login with different usernames in each client")
    print("4. In the server terminal, test these commands:")
    print("   - Type 'list' to see all connected clients")
    print("   - Type 'count' to see client count")
    print("   - Type 'exit' to shutdown")
    print()
    print("5. Observe the client tracking information:")
    print("   - Client ID, Username, Address, Status, Connected time")
    print("   - Automatic client count display every 30 seconds")
    print("   - Real-time updates when clients connect/disconnect")
    print("=" * 60)

if __name__ == "__main__":
    print("Lab 06 - Task 03: Client Tracking Test")
    print("Choose test method:")
    print("1. Automated test")
    print("2. Manual test instructions")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_client_tracking()
    elif choice == "2":
        test_manual_client_tracking()
    else:
        print("Invalid choice. Running automated test...")
        test_client_tracking()
