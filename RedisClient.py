import socket as s
import json


PORT = 3031
IP = '127.0.0.1'

SET = 'set'
GET = 'get'
SEARCH = 'search'
OK = 'ok'
TAKEN = 'taken'
GOODBYE = 'good bye'
UNKNOWN_COMMAND = 'unknown command'

COMMANDS = {}

class Client(object):
    def __init__(self, socket=None, address=('127.0.0.1', 3030)):
        if socket == None:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket = socket
        self.address = address
        self.startConnection()
        self.name = None

    def log(self,text):
        print text

    def connect(self):
        self.socket.connect(self.address)
        self.log("connection to address {} status: {}".format(self.address, self.receive()))

    def getName(self):
        return raw_input('Enter your name: ')

    def receive(self):
        return self.socket.recv(4096)

    def send(self, text):
        self.socket.sendall(text)

    def set(self):
        key = raw_input("enter key: ")
        value = raw_input("enter value: ")
        dict = {key: value}
        message = {SET: dict}
        # print 'for testing: this was sent - {}'.format(message)
        self.send(json.dumps(message))
        return self.receive()
    COMMANDS[SET] = set

    def get(self):
        key = raw_input("enter requested key: ")
        message = {GET: key}
        self.send(json.dumps(message))
        return self.receive()
    COMMANDS[GET] = get

    def search(self):
        str = raw_input("enter string to search: ")
        message = {SEARCH: str}
        self.send(json.dumps(message))
        return self.receive()
    COMMANDS[SEARCH] = search

    def sendName(self, name):
        self.send(name)
        response = self.receive()
        if response == TAKEN:
            self.log("name '{}' is already taken")
            return
        self.log('name was accepted :)\n')

    def printCommandsList(self):
        for i in range(len(COMMANDS)):
            self.log('{}. {}'.format(i, COMMANDS.keys()[i]))

    def enterCommand(self):
        self.printCommandsList()
        command_number = raw_input('Enter command number: ')
        command_number = int(command_number)
        command_name = COMMANDS.keys()[command_number]
        command_func = COMMANDS[command_name]
        return command_func(self)

    def printResponse(self, response):
        self.log('response from server: {}'.format(response))

    def startConnection(self):
        self.connect()
        self.name = self.getName()
        self.sendName(self.name)
        response = self.enterCommand()
        while response != GOODBYE:
            self.printResponse(response)
            response = self.enterCommand()
        print 'close connection...'
        return

def main():
    c = Client(address = (IP, PORT))

if __name__ == "__main__":
    main()

