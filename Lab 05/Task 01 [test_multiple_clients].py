#!/usr/bin/env python3
"""
Lab 05 - Task 01: Test Script for Multiple Clients
Automatically runs 5 clients to test server with backlog=3.
"""

import subprocess
import time
import sys
import os

def run_client(client_id, delay=0):
    """Run a single client instance"""
    try:
        print(f"Starting Client {client_id}...")
        
        # Add delay to stagger client connections
        if delay > 0:
            time.sleep(delay)
        
        # Run the client script
        client_script = os.path.join(os.path.dirname(__file__), "simple_client.py")
        process = subprocess.Popen(
            [sys.executable, client_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send some test messages
        test_messages = [
            f"Hello from Client {client_id}",
            f"Testing message {client_id}",
            "quit"
        ]
        
        for msg in test_messages:
            process.stdin.write(msg + "\n")
            process.stdin.flush()
            time.sleep(0.5)  # Small delay between messages
        
        # Wait for process to complete
        stdout, stderr = process.communicate(timeout=10)
        
        print(f"Client {client_id} output:")
        print(stdout)
        if stderr:
            print(f"Client {client_id} errors:")
            print(stderr)
            
    except subprocess.TimeoutExpired:
        print(f"Client {client_id} timed out")
        process.kill()
    except Exception as e:
        print(f"Error running Client {client_id}: {e}")

def main():
    """Main function to test multiple clients"""
    print("Lab 05 - Task 01: Testing Multiple Clients")
    print("=" * 50)
    print("This script will run 5 clients to test the server with backlog=3")
    print("Make sure the server is running first!")
    print()
    
    # Check if server script exists
    server_script = os.path.join(os.path.dirname(__file__), "iterated_server.py")
    if not os.path.exists(server_script):
        print("Error: iterated_server.py not found!")
        return
    
    # Check if client script exists
    client_script = os.path.join(os.path.dirname(__file__), "simple_client.py")
    if not os.path.exists(client_script):
        print("Error: simple_client.py not found!")
        return
    
    print("Starting 5 clients with staggered connections...")
    print("(Each client will connect with a 1-second delay)")
    print()
    
    # Run 5 clients with staggered timing
    for i in range(1, 6):
        run_client(i, delay=i-1)  # Stagger by 1 second each
        print(f"Client {i} completed")
        print("-" * 30)
    
    print("All clients completed!")
    print("\nNote: With backlog=3, only 3 clients should be able to connect")
    print("simultaneously. The other 2 should wait or be queued.")

if __name__ == "__main__":
    main()
