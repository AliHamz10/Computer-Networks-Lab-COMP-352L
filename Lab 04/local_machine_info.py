"""
Local Machine Information
------------------------
Displays the host name and IP address of the local machine using Python's socket library.
Efficient, robust, and well-commented for clarity and maintainability.
"""

import socket


def print_machine_info():
    """
    Prints the local machine's host name and IP address.
    Handles exceptions gracefully and provides clear output.
    """
    try:
        # Get the host name of the local machine
        host_name = socket.gethostname()
        # Get the IP address associated with the host name
        ip_address = socket.gethostbyname(host_name)
        print(f"Host name: {host_name}")
        print(f"IP address: {ip_address}")
    except socket.error as err:
        print(f"Unable to retrieve machine info: {err}")

if __name__ == '__main__':
    print_machine_info()
