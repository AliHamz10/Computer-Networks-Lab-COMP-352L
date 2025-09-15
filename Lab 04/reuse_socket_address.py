#!/usr/bin/env python
#

import socket


sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Get the old state of the SO_REUSEADDR option
old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
print (f"Old sock state: {old_state}")

# Enable the SO_REUSEADDR option
sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
new_state = sock.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
print (f"New sock state: {new_state}")

local_port = 8282

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f"srv socket state: {srv.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )}")
srv.bind( ('', local_port) )
srv.listen(1)
print (f"Listening on port: {local_port}")

connection, addr = srv.accept()
print (f"Connected by {addr[0]}: {addr[1]}")







