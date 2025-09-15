#!/usr/bin/env python3
"""
Quick Chat - Just enter IP and chat!
"""
import socket

def chat_with_friend():
    # Get friend's IP
    friend_ip = input("Enter friend's IP (e.g., 10.1.30.113): ").strip()
    if not friend_ip:
        print("No IP provided!")
        return
    
    port = 8000
    
    try:
        # Connect to friend
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((friend_ip, port))
        
        print(f"✅ Connected to {friend_ip}")
        print("💬 Start typing messages!")
        print("Type 'quit' to exit")
        print("-" * 30)
        
        while True:
            # Send message
            message = input("You: ")
            if message.lower() == 'quit':
                break
            sock.send(message.encode('utf-8'))
            
            # Get response
            response = sock.recv(1024).decode('utf-8')
            print(f"Friend: {response}")
            
    except ConnectionRefusedError:
        print(f"❌ Can't connect to {friend_ip}")
        print("Tell your friend to run: python3 quick_server.py")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    chat_with_friend()
