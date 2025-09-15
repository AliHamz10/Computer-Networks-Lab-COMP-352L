"""
Service Name Finder
------------------
This script demonstrates how to retrieve the service name for a given port number and transport layer protocol using Python's socket library.
"""

import socket

# List of (port, protocol) tuples to check
services = [
    (80, 'tcp'),   # HTTP over TCP
    (25, 'tcp'),   # SMTP over TCP
    (53, 'udp'),   # DNS over UDP
]

def get_service_name(port, protocol):
    """
    Returns the service name for a given port and protocol.
    If the service is not found, returns 'Unknown'.
    """
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return 'Unknown'

# Iterate over the list and print service names
for port, protocol in services:
    service_name = get_service_name(port, protocol)
    print(f"Port: {port} ({protocol.upper()}) => service name: {service_name}")
