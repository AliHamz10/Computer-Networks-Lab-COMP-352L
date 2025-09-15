"""
Socket Timeout Demonstration
---------------------------
Shows how to get and set the timeout value for a TCP socket in Python.
Efficient, robust, and well-commented for clarity and maintainability.
"""

import socket

def test_socket_timeout():
    """
    Creates a TCP socket, displays its default timeout,
    sets a new timeout, and displays the updated value.
    Handles exceptions gracefully.
    """
    try:
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Display the default timeout (None means blocking mode)
        print(f"Default socket timeout: {s.gettimeout()}")
        # Set a new timeout value (in seconds)
        timeout_value = 10.0
        s.settimeout(timeout_value)
        print(f"Current socket timeout: {s.gettimeout()} seconds")
    except socket.error as err:
        print(f"Socket error: {err}")
    finally:
        s.close()  # Ensure the socket is closed

if __name__ == '__main__':
    test_socket_timeout()
