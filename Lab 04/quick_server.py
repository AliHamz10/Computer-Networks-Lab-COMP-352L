#!/usr/bin/env python3
"""
Quick Server - For your friend to run
"""
import socket

def start_server():
    port = 8000
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(1)
        
        print(f"🚀 Server started on port {port}")
        print("📡 Waiting for friend to connect...")
        
        client, address = server.accept()
        print(f"✅ Friend connected from {address[0]}")
        print("💬 Start chatting!")
        print("-" * 30)
        
        while True:
            # Get message from friend
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
        print(f"Error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
