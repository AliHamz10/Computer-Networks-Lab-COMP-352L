#!/usr/bin/env python
# get service name from port number and transport layer protocol

import socket


for port in [80, 25]:
    print ("Port: %s => service name: %s" %(port, socket.getservbyport(port, 'tcp')))

print ("Port: %s => service name: %s" %(53, socket.getservbyport(53, 'udp')))
    

