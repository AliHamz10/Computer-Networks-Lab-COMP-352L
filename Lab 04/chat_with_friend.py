#!/usr/bin/env python3
"""
Chat with Friend - Direct IP Version
------------------------------------
Simple chat where you enter your friend's IP and start chatting.
"""
import socket
import threading
import sys

def send_message_to_friend(friend_ip, port=8000):
    """Send a message to your friend"""
    try:
        # Create socket and connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((friend_ip, port))
        
        print(f"✅ Connected to {friend_ip}:{port}")
        print("💬 Type your message and press Enter")
        print("💡 Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            # Get message from user
            message = input("You: ")
            
            if message.lower() == 'quit':
                break
                
            # Send message
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(1024).decode('utf-8')
            print(f"Friend: {response}")
            
    except ConnectionRefusedError:
        print(f"❌ Could not connect to {friend_ip}:{port}")
        print("Make sure your friend is running the server!")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        sock.close()
        print("👋 Disconnected!")

def start_server_for_friend(port=8000):
    """Start server to receive messages from friend"""
    try:
        # Create server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(1)
        
        print(f"🚀 Server started on port {port}")
        print("📡 Waiting for your friend to connect...")
        print("💡 Press Ctrl+C to stop")
        print("-" * 40)
        
        # Accept connection
        client, address = server.accept()
        print(f"✅ Friend connected from {address[0]}:{address[1]}")
        print("💬 Start chatting!")
        print("-" * 30)
        
        while True:
            # Receive message
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
                
            print(f"Friend: {message}")
            
            # Send response
            response = input("You: ")
            if response.lower() == 'quit':
                break
                
            client.send(response.encode('utf-8'))
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server.close()

def main():
    print("💬 Chat with Friend")
    print("=" * 30)
    
    # Get friend's IP
    friend_ip = input("Enter your friend's IP address: ").strip()
    
    if not friend_ip:
        print("❌ No IP address provided!")
        return
    
    print(f"\nFriend's IP: {friend_ip}")
    print("Choose what to do:")
    print("1. Send message to friend")
    print("2. Start server (wait for friend to connect)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        send_message_to_friend(friend_ip)
    elif choice == "2":
        start_server_for_friend()
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
