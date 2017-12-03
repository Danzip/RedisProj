import socket as s
import thread
import sys
import json
import threading

OK = 'ok'
TAKEN = 'taken'
GET = 'get'
SET = 'set'
SEARCH = 'search'
UNKNOWN_COMMAND = 'unknown command'
NOT_FOUND = 'not found'
GOODBYE = 'good bye'
IP = '127.0.0.1'
PORT = 3030
SHUTDOWN='shutdown'
SHOW_CLIENTS='show_clients'
FLUSH_DB= 'flush db'
CLEAN_DB='clean db'

class DB(object):
    def __init__(self,file='backup.txt'):
        self.dict = {}
        self.backup_file=file
        self.loadFromBackUp()

    def cleanData(self):
        self.dict={}
        self.backupData()

    def loadFromBackUp(self):
        f=open(self.backup_file,'r')
        data=f.read()
        lines=data.split('\n')
        for line in lines:
            if ' : ' in line:
                key,value=line.split(' : ')
                self.dict[key]=json.loads(value)

    def setData(self, key, value):
        self.dict[key] = value

    def getData(self, key):
        try:
            # print 'Added successfully'
            return self.dict[key]
        except(KeyError):
            return False
            # print "Error: Key doesn't exist"

    def search(self, text):
        output = []
        for key in self.dict.keys():
            if key.startswith(text):
                output.append(key)
        return output

    def backupData(self):
        f = open(self.backup_file, 'w')
        for key in self.dict:
            f.write("{} : {}\n".format(key,json.dumps(self.dict[key])))
        f.close()



class Client(object):
    def __init__(self, socket, address, name=None):
        self.socket = socket
        self.address = address
        self.name = name

    def add_name(self, name):
        self.name = name


class ConnectionHandler(object):
    def __init__(self, server, socket, address):
        self.server = server
        self.socket = socket
        self.address = address
        #self.handleConnection()

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
        client = Client(client_socket, client_address)
        return client

    def send_to_client(self, client, data):
        client.socket.send(data)

    def recv_from_client(self, client):
        return client.socket.recv(4096)

    def handleConnection(self):
        self.bind()
        self.listen()
        while self.server.server_up:
            client=self.accept()
            # print "handle connection on"
            d = threading.Thread(target=self.clientHandler, args=(client,))
            d.daemon = True
            d.start()
            # print self.server.server_up


    def clientHandler(self, client):
        self.send_to_client(client, OK)
        name = self.recv_from_client(client)
        self.log("received name: '{}'".format(name))

        success = self.server.add_client(name, client)
        if not success:
            self.send_to_client(client, TAKEN)
            client.socket.close()
            self.log('name is already taken. closing connection')
            return
        self.send_to_client(client, OK)
        self.commandsHandler(client)


    def recv_command(self, client):
        command = self.recv_from_client(client)
        if command == '':
            return command
        unpacked_command = json.loads(command)
        return unpacked_command

    def send_answer(self, client, answer):
        packed_answer = json.dumps(answer)
        self.send_to_client(client, packed_answer)

    def commandsHandler(self, client):
        command = self.recv_command(client)
        while command != GOODBYE and command != '' and self.server.server_up:
            # print "commandsHANDLEr ON"
            command_action = command.keys()[0]
            command_values = command[command_action]
            if command_action == SET:
                key_to_set = command_values.keys()[0]
                values_to_set = command_values[key_to_set]
                server_response = self.server.setData(key_to_set, values_to_set)
                self.send_answer(client, OK)
            elif command_action == GET:
                server_response = self.server.getData(command_values)
                if server_response == False:
                    self.send_answer(client, NOT_FOUND)
                else:
                    self.send_answer(client, server_response)
            elif command_action == SEARCH:
                server_response = self.server.search(command_values)
                self.send_answer(client, server_response)
            else :
                self.send_answer(client,UNKNOWN_COMMAND)
            command = self.recv_command(client)
        client.socket.close()


class Server(object):  # sends request to database,receives answer sends answer to translator
    def __init__(self, address, socket=None, clients={}):
        self.clients = clients
        self.server_up = True
        self.socket = socket
        if socket == None:
            self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.data_base = DB()
        self.connection_handler = ConnectionHandler(self, self.socket, address)
        IO_thread = threading.Thread(target=self.handleIO,args=())
        IO_thread.daemon = False
        IO_thread.start()
        db_thread = threading.Thread(target=self.databaseHandler,args=())
        db_thread.daemon = True
        db_thread.start()
        iWishItWork = threading.Thread(target=self.connection_handler.handleConnection,args=())
        iWishItWork.daemon = True
        iWishItWork.start()
    def log(self,data):
        print data

    def databaseHandler(self,time =10.0):
        t = threading.Timer(time, self.databaseHandler)
        if self.server_up:
            t.start()
            #print("backing up data")
            self.data_base.backupData()
        else:
            t.cancel()

    def add_client(self, name, client):
        if name not in self.clients.keys():
            self.clients[name] = client
            return True
        return False

    def handleIO(self):
        command=raw_input("enter command:")
        while command!=SHUTDOWN:
            command=raw_input("enter command:")
            if command== SHOW_CLIENTS:
                for client in self.clients:
                    print client
            if command== FLUSH_DB:
                self.data_base.backupData()
                self.log('flushed successfully !')
            if command== CLEAN_DB:
                self.data_base.cleanData()
                self.log('cleaned successfully !')

        for client in self.clients:
            self.clients[client].socket.close()
        self.socket.close()
        self.server_up = False
        return

    def setData(self, key, value):
        self.data_base.setData(key, value)

    def getData(self, key):
        return self.data_base.getData(key)

    def search(self, text):
        return self.data_base.search(text)



def main():
    server_address = (IP, PORT)
    server = Server(server_address)


if __name__ == "__main__":
    main()


