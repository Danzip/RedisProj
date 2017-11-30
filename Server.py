import socket as s
import threading
import sys
import json


class Server(object):
    def __init__(self, server_ip, server_port, socket=None, clients=None):
        self.addr = (server_ip, server_port)
        if socket == None:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket = socket
        self.clients = clients

    def log(self, text):
        print >> sys.stderr, text

    def listen(self, slots=5):
        self.socket.listen(slots)
        self.log('Started listing with {} slots to address {}'.format(slots, self.addr))

    def bind(self):
        self.socket.bind(self.addr)
        self.log("Server's socket is bound to {}".format(self.addr))

    def accept(self):
        client_socket, client_address = self.socket.accept()
        self.log('Accepted new client with address {}'.format(client_address))
        self.clients.append(Client(client_socket, client_address))

    def send(self,client,data):
        client.socket.send(data)

    def recv(self,client):
        return client.socket.recv(1024)



class Client(object):
    def __init__(self, socket, address, name=None):
        self.socket = socket
        self.address = address
        self.name = name

    def add_name(self, name):
        self.name = name
