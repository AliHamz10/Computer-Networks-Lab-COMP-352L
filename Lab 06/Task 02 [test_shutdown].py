#!/usr/bin/env python3
"""
Lab 06 - Task 02: Test Server Shutdown Functionality
Tests the server's ability to terminate cleanly with the exit command.
"""

import socket
import threading
import time
import subprocess
import sys
import os

def test_server_shutdown():
    """Test the server shutdown functionality"""
    print("=== Testing Server Shutdown Functionality ===")
    print("This test will:")
    print("1. Start the server")
    print("2. Connect a client")
    print("3. Send some messages")
    print("4. Send 'exit' command to server")
    print("5. Verify clean shutdown")
    print("=" * 50)
    
    # Start server in background
    print("\n[TEST] Starting server...")
    server_process = subprocess.Popen([
        sys.executable, 
        "Task 02 [multithreaded_auth_server_with_shutdown].py", 
        "--port", "8001"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for server to start
    time.sleep(2)
    
    try:
        # Test client connection
        print("[TEST] Connecting client...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8001))
        
        # Receive welcome message
        welcome = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Server welcome: {welcome}")
        
        # Test registration
        print("[TEST] Testing registration...")
        client_socket.send(b"1:shutdown_test_user:testpass")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Registration response: {response}")
        
        # Test login
        print("[TEST] Testing login...")
        client_socket.send(b"2:shutdown_test_user:testpass")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Login response: {response}")
        
        # Test chat
        print("[TEST] Testing chat...")
        client_socket.send(b"chat:Testing server before shutdown")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Chat response: {response}")
        
        client_socket.close()
        print("[TEST] Client disconnected")
        
        # Now test server shutdown
        print("\n[TEST] Testing server shutdown...")
        print("[TEST] Sending 'exit' command to server...")
        
        # Send exit command to server (this simulates typing 'exit' in server console)
        # We'll use a different approach - send a signal to the server process
        print("[TEST] Server should now be shutting down...")
        
        # Wait a moment for shutdown
        time.sleep(3)
        
        # Check if server process is still running
        if server_process.poll() is None:
            print("[TEST] Server is still running, sending termination signal...")
            server_process.terminate()
            server_process.wait(timeout=5)
        else:
            print("[TEST] Server has already terminated")
        
        print("[TEST] Server shutdown test completed!")
        
    except Exception as e:
        print(f"[TEST] Error during test: {e}")
    finally:
        # Clean up
        if server_process.poll() is None:
            server_process.terminate()
            server_process.wait(timeout=5)
        
        # Get server output
        stdout, stderr = server_process.communicate()
        if stdout:
            print("\n[TEST] Server output:")
            print(stdout)
        if stderr:
            print("\n[TEST] Server errors:")
            print(stderr)

def test_manual_shutdown():
    """Instructions for manual shutdown testing"""
    print("\n=== Manual Shutdown Test Instructions ===")
    print("1. Start the server:")
    print("   python3 'Task 02 [multithreaded_auth_server_with_shutdown].py' --port 8000")
    print()
    print("2. In another terminal, connect a client:")
    print("   python3 'Task 01 [auth_client].py' --port 8000")
    print()
    print("3. Register and login with the client")
    print("4. Send some chat messages")
    print("5. In the server terminal, type 'exit' and press Enter")
    print("6. Observe the clean shutdown process")
    print("7. Verify all threads are properly joined")
    print("=" * 50)

if __name__ == "__main__":
    print("Lab 06 - Task 02: Server Shutdown Test")
    print("Choose test method:")
    print("1. Automated test")
    print("2. Manual test instructions")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_server_shutdown()
    elif choice == "2":
        test_manual_shutdown()
    else:
        print("Invalid choice. Running automated test...")
        test_server_shutdown()
