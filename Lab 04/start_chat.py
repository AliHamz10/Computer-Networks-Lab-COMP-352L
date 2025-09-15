#!/usr/bin/env python3
"""
Quick Chat Setup
----------------
Easy way to start chatting with your friend
"""
import subprocess
import sys
import os

def start_server():
    """Start the chat server"""
    print("🚀 Starting chat server...")
    print("=" * 40)
    try:
        subprocess.run([sys.executable, "chat_server.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")

def start_client():
    """Start the chat client"""
    print("💬 Starting chat client...")
    print("=" * 40)
    
    # Get friend's IP
    friend_ip = input("Enter your friend's IP address: ").strip()
    if not friend_ip:
        print("No IP provided. Exiting.")
        return
    
    # Get nickname
    nickname = input("Enter your nickname: ").strip()
    if not nickname:
        nickname = "Anonymous"
    
    # Prepare input for chat client
    input_data = f"{friend_ip}\n8000\n{nickname}\n"
    
    try:
        subprocess.run(
            [sys.executable, "chat_client.py"],
            input=input_data,
            text=True
        )
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

def main():
    print("💬 Two-Way Chat System")
    print("=" * 30)
    print("1. Start Server (Host)")
    print("2. Start Client (Join)")
    print("3. Exit")
    
    choice = input("\nChoose option (1-3): ").strip()
    
    if choice == "1":
        start_server()
    elif choice == "2":
        start_client()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
