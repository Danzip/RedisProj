import socket as s
import threading
import sys
import json

OK = 'ok'
TAKEN = 'taken'
GET = 'get'
SET = 'set'
SEARCH = 'search'
UNKNOWN_COMMAND = 'unknown command'
NOT_FOUND ='not found'


class DB(object):
    def __init__(self):
        self.dict = {}

    def addData(self, key, value):
        self.dict[json.dumps(key)] = json.dumps(value)

    def getData(self, key):
        try:
            #print 'Added successfully'
            return json.loads(self.dict[json.dumps(key)])
        except(KeyError):
            return False
            #print "Error: Key doesn't exist"

    def search(self, text):
        output = []
        for key in self.dict.keys():
            if key.startswith(text):
                output.append(key)
        return output


class Server(object):
    def __init__(self, server_address, socket=None):
        self.address = server_address
        if socket == None:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket = socket
        self.clients = {}
        self.socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
        self.data_base = DB()

    def add_client(self, client_dict):
        self.clients.update(client_dict)

    def log(self, text):
        print >> sys.stderr, text

    def listen(self, slots=5):
        self.socket.listen(slots)
        self.log('Started listing with {} slots to address {}'.format(slots, self.address))

    def bind(self):
        self.socket.bind(self.address)
        self.log("Server's socket is bound to {}".format(self.address))

    def accept(self):
        client_socket, client_address = self.socket.accept()
        self.log('Accepted new client with address {}'.format(client_address))
        self.handle_client_con(client_socket,client_address)

    def send(self, client, data):
        client.socket.send_to_client(data)

    def recv(self, client):
        return client.socket.recv_from_client(4096)


    def handle_client_con(self, client_socket, client_address):
        self.send(self.clients[0], OK)
        name = self.recv(self.clients[0])
        self.log("received name: '{}'".format(name))
        # if (name_exists):
        #     pass

        new_client=Client(client_socket, client_address, name)
        new_client_dict={name: new_client}
        self.add_client(new_client_dict)
        self.handle_client_commands()

    def set_data(self, dict_to_set):
        key_to_add = dict_to_set.keys()[0]
        data_to_add = dict_to_set[key_to_add]
        self.data_base[key_to_add] = data_to_add
        self.pack_and_send(OK)

    def get_data(self,key):
        if key in self.data_base:
            self.pack_and_send(self.data_base[key])
        else:
            self.pack_and_send(NOT_FOUND)

    def search_key(self):



    def handle_client_commands(self):
        command=self.receive_and_unpack()
        action = command.keys()[0]
        values = command[action]
        if action == SET:
            self.set_data(values)
        elif action==GET:
            self.get_data(values.keys()[0])
        elif action==SEARCH:
            self.search_key(values)


    def pack_and_send(self, data):
        packed_msg = json.dumps(data)
        self.send(packed_msg)

    def receive_and_unpack(self):
        packed = self.recv()
        return json.loads(packed)




class Client(object):
    def __init__(self, socket, address, name=None):
        self.socket = socket
        self.address = address
        self.name = name

    def add_name(self, name):
        self.name = name








# def send_command(self):


def main():
    server_address = ('127.0.0.1', 3031)
    server = Server(server_address)
    server.bind()
    server.listen()
    server.accept()
    server.socket.close()


# >>>>>>> 6fc5107a1d88f6c7a58525b7c65015f207eb18b8

if __name__ == "__main__":
    main()
