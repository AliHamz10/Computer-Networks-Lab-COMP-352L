#!/usr/bin/env python3
"""
Lab 05 - Task 01: Simple TCP Client
Connects to server and communicates with auto-determined client number.
"""

import socket
import time
import argparse
import random

class SimpleClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = None
        self.client_number = None
        
    def connect_to_server(self):
        """Connect to the server and start communication"""
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to server
            print(f"Connecting to server at {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            print("Connected to server!")
            
            # Receive welcome message to get client number
            welcome_msg = self.socket.recv(1024).decode('utf-8')
            print(f"Server says: {welcome_msg}")
            
            # Extract client number from welcome message
            if "Client" in welcome_msg:
                try:
                    # Extract number from "Connected to Client X"
                    self.client_number = int(welcome_msg.split()[-1])
                    print(f"I am Client {self.client_number}")
                except:
                    self.client_number = random.randint(1, 100)  # Fallback
                    print(f"Could not determine client number, using {self.client_number}")
            else:
                self.client_number = random.randint(1, 100)
                print(f"Using random client number: {self.client_number}")
            
            # Start communication loop
            self.communicate()
            
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure server is running.")
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            self.cleanup()
    
    def communicate(self):
        """Communicate with server - send messages and receive responses"""
        print(f"\nClient {self.client_number} ready to communicate!")
        print("Type messages to send to server (or 'quit' to exit)")
        
        try:
            # Send initial message with client number
            initial_msg = f"Client {self.client_number}"
            self.socket.send(initial_msg.encode('utf-8'))
            print(f"Sent: {initial_msg}")
            
            # Receive response
            response = self.socket.recv(1024).decode('utf-8')
            print(f"Received: {response}")
            
            # Interactive communication
            while True:
                try:
                    # Get user input
                    message = input(f"Client {self.client_number}> ")
                    
                    if message.lower() in ['quit', 'exit', 'q']:
                        print("Disconnecting...")
                        break
                    
                    # Send message to server
                    self.socket.send(message.encode('utf-8'))
                    print(f"Sent: {message}")
                    
                    # Receive response
                    response = self.socket.recv(1024).decode('utf-8')
                    print(f"Server response: {response}")
                    
                except KeyboardInterrupt:
                    print("\nDisconnecting...")
                    break
                except Exception as e:
                    print(f"Communication error: {e}")
                    break
                    
        except Exception as e:
            print(f"Communication error: {e}")
    
    def cleanup(self):
        """Clean up client resources"""
        if self.socket:
            self.socket.close()
            print("Client socket closed")

def main():
    """Main function to run the client"""
    parser = argparse.ArgumentParser(description='Simple TCP Client for Lab 05')
    parser.add_argument('--host', default='localhost', help='Server host (default: localhost)')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
    
    args = parser.parse_args()
    
    # Create and start client
    client = SimpleClient(args.host, args.port)
    client.connect_to_server()

if __name__ == "__main__":
    main()
