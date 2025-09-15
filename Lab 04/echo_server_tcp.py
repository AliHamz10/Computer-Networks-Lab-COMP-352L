# A Trivial TCP Server using sockets
# It receives a message from a client.
# Echoes the message back and terminates.

import socket


host = 'localhost'
data_payload = 10 # how many bytes to receive
port = 8000



# Create a TCP socket
# AF.INET: IPv4, SOCK_STREAM: TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enable reuse address/port 
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind the socket to the port
server_address = (host, port)
print (f"Starting up echo server  on {host} port {port}")
sock.bind(server_address)


# Listen to clients
sock.listen() 

print ("Waiting to receive message from client")
client, address = sock.accept()

data = client.recv(data_payload)
print (f"Data: {data}")
data = client.recv(data_payload)
print (f"Data: {data}")
data = client.recv(data_payload)
print (f"Data: {data}")


client.send(data)
print (f"sent {len(data)} bytes back to {address}")
# end connection
client.close()
sock.close() 
   

