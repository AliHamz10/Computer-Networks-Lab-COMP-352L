#!/usr/bin/env python
# Find the ip address of a remote machine
# using its domain name


import socket


remote_host = 'www.python.org'

print (f"IP address of {remote_host} : {socket.gethostbyname(remote_host)}")


    

