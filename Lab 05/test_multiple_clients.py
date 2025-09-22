#!/usr/bin/env python3
"""
Script to test multiple client connections to the server
This will help demonstrate the backlog behavior with 5 clients
"""

import subprocess
import time
import threading

def run_client(client_number):
    """Run a single client in a separate process"""
    try:
        result = subprocess.run(
            ['python3', 'simple_client.py', str(client_number)],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(f"Client {client_number} output:")
        print(result.stdout)
        if result.stderr:
            print(f"Client {client_number} errors:")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f"Client {client_number} timed out")
    except Exception as e:
        print(f"Client {client_number} error: {e}")

def main():
    print("Starting 5 clients to test server backlog...")
    print("Make sure the server is running first!")
    print("=" * 50)
    
    # Start all 5 clients simultaneously
    threads = []
    for i in range(1, 6):
        thread = threading.Thread(target=run_client, args=(i,))
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Small delay between client starts
    
    # Wait for all clients to complete
    for thread in threads:
        thread.join()
    
    print("=" * 50)
    print("All clients completed")

if __name__ == "__main__":
    main()
