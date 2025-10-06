#!/usr/bin/env python3
"""
Lab 06 - Task 01: Simple Test Script
Tests the server with a single client for registration and login.
"""

import socket
import time

def test_server():
    """Test the server with simple socket communication"""
    try:
        # Connect to server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8000))
        print("[TEST] Connected to server")
        
        # Receive welcome message
        welcome = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Server welcome: {welcome}")
        
        # Test registration
        print("\n[TEST] Testing registration...")
        client_socket.send(b"1:testuser:testpass")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Registration response: {response}")
        
        # Test login
        print("\n[TEST] Testing login...")
        client_socket.send(b"2:testuser:testpass")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Login response: {response}")
        
        # Test chat
        print("\n[TEST] Testing chat...")
        client_socket.send(b"chat:Hello from test client!")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Chat response: {response}")
        
        # Test logout
        print("\n[TEST] Testing logout...")
        client_socket.send(b"logout")
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[TEST] Logout response: {response}")
        
        client_socket.close()
        print("\n[TEST] Test completed successfully!")
        
    except Exception as e:
        print(f"[TEST] Error: {e}")

if __name__ == "__main__":
    test_server()
