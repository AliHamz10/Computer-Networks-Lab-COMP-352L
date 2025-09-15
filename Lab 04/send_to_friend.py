#!/usr/bin/env python3
"""
Quick script to send message to friend
"""
import subprocess
import sys

def send_message_to_friend():
    friend_ip = "10.1.30.113"
    port = "8000"
    message = input("Enter your message: ")
    
    # Prepare input for the message client
    input_data = f"{friend_ip}\n{port}\n{message}\n"
    
    try:
        # Run the message client with the input
        result = subprocess.run(
            ["python3", "message_client.py"],
            input=input_data,
            text=True,
            cwd="/Users/alihamza/PycharmProjects/Computer-Networks-Lab-COMP-352L/Lab 04"
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("📱 Sending message to friend at 10.1.30.113")
    print("=" * 50)
    send_message_to_friend()
