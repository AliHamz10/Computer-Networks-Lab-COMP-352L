#!/usr/bin/env python3
"""
Lab 06 - Task 04: Test Group Chat Functionality
Tests the server's group chat and broadcast functionality with multiple clients.
"""

import socket
import threading
import time
import subprocess
import sys
import os

def test_group_chat():
    """Test the group chat functionality"""
    print("=== Testing Group Chat Functionality ===")
    print("This test will:")
    print("1. Start the server with group chat")
    print("2. Connect multiple clients")
    print("3. Register and login users")
    print("4. Join chat room")
    print("5. Test broadcast messages")
    print("6. Verify sender ID in messages")
    print("=" * 60)
    
    # Start server in background
    print("\n[TEST] Starting server with group chat...")
    server_process = subprocess.Popen([
        sys.executable, 
        "Task 04 [multithreaded_auth_server_with_group_chat].py", 
        "--port", "8003"
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
            client_socket.connect(('127.0.0.1', 8003))
            
            # Receive welcome message
            welcome = client_socket.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} connected: {welcome[:50]}...")
            
            clients.append(client_socket)
            time.sleep(0.5)  # Small delay between connections
        
        print(f"[TEST] Connected {len(clients)} clients")
        
        # Test registration and login for each client
        usernames = []
        for i, client in enumerate(clients):
            username = f"groupchat_user_{i+1}"
            password = f"testpass_{i+1}"
            usernames.append(username)
            
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
        
        # Join chat room
        print("[TEST] Joining chat room...")
        for i, client in enumerate(clients):
            client.send(b"3")  # Join chat
            response = client.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} join chat: {response[:50]}...")
            time.sleep(0.5)
        
        print("[TEST] All clients joined chat room")
        
        # Test broadcast messages
        print("\n[TEST] Testing broadcast messages...")
        for i, client in enumerate(clients):
            message = f"Hello everyone from {usernames[i]}!"
            client.send(f"broadcast:{message}".encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            print(f"[TEST] Client {i+1} broadcast: {response[:50]}...")
            time.sleep(1)
        
        print("\n[TEST] Group chat test completed!")
        print("[TEST] Check server terminal for broadcast messages with sender IDs")
        print("[TEST] In server terminal, type:")
        print("  - 'chatroom' to see chat room members")
        print("  - 'list' to see all connected clients")
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
            print("\n[TEST] Server is still running. You can test group chat manually.")
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

def test_manual_group_chat():
    """Instructions for manual group chat testing"""
    print("\n=== Manual Group Chat Test Instructions ===")
    print("1. Start the server with group chat:")
    print("   python3 'Task 04 [multithreaded_auth_server_with_group_chat].py' --port 8000")
    print()
    print("2. In multiple terminals, connect clients:")
    print("   python3 'Task 04 [group_chat_client].py' --port 8000")
    print()
    print("3. In each client:")
    print("   - Register and login with different usernames")
    print("   - Join chat room (option 3)")
    print("   - Send broadcast messages (option 4 or 'broadcast:message')")
    print()
    print("4. In the server terminal, test these commands:")
    print("   - Type 'chatroom' to see chat room members")
    print("   - Type 'list' to see all connected clients")
    print("   - Type 'exit' to shutdown")
    print()
    print("5. Observe the group chat functionality:")
    print("   - Broadcast messages sent to all clients")
    print("   - Sender ID included in messages")
    print("   - Real-time group communication")
    print("=" * 60)

if __name__ == "__main__":
    print("Lab 06 - Task 04: Group Chat Test")
    print("Choose test method:")
    print("1. Automated test")
    print("2. Manual test instructions")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_group_chat()
    elif choice == "2":
        test_manual_group_chat()
    else:
        print("Invalid choice. Running automated test...")
        test_group_chat()
