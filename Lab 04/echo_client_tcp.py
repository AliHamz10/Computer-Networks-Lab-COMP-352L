# A simple TCP client using sockets
# Establishes a connection to a server.
# Sends a message.
# Receives a reply and terminates.

import socket



host = 'localhost'
port = int(input("Enter server port: "))

""" A simple echo client """
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server
server_address = (host, port)
print (f"Connecting to {host} port {port}")
sock.connect(server_address)

# Send data

# Send data
message = "Test message. This will be echoed"
print (f"Sending {message}")
sock.sendall(message.encode('utf-8'))
# Look for the response

data = sock.recv(256)

print (f"Received: {data}")


print ("Closing connection to the server")
sock.close()


