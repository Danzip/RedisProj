import socket as s
import threading
import sys
import json


class DB(object):
    def __init__(self):
        self.dict = {}


    def addData(self, key, value):
        self.dict[json.dumps(key)] = json.dumps(value)


    def getData(self, key):
        try:
            print 'Added successfully'
            return json.loads(self.dict[json.dumps(key)])
        except(KeyError):
            print "Error: Key doesn't exist"


    def search(self, text):
        output = []
        for key in self.dict.keys():
            if key.startswith(text):
                output.append(key)
        return output


class Server(object):
    def __init__(self, server_ip, server_port, socket=None, clients=[]):
        self.addr = (server_ip, server_port)
        if socket == None:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket = socket
        self.clients = clients
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

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

    def send(self, client, data):
        client.socket.send(data)

    def recv(self, client):
        return client.socket.recv(1024)


class Client(object):
    def __init__(self, socket, address, name=None):
        self.socket = socket
        self.address = address
        self.name = name

    def add_name(self, name):
        self.name = name


def main():
    server_ip = '127.0.0.1'
    server_port = 3031
    server = Server(server_ip, server_port)
    server.bind()
    server.listen()
    server.accept()
    server.socket.close()
    server.send(server.clients[0], "hi")
    name = server.recv(server.clients[0])
    server.log("received name: '{}'".format(name))

#>>>>>>> 6fc5107a1d88f6c7a58525b7c65015f207eb18b8

if __name__ == "__main__":
    main()
