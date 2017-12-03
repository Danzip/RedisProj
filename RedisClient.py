import socket as s
import json


PORT = 3031
IP = '127.0.0.1'

SET = 'set'
GET = 'get'
SEARCH = 'search'
OK = 'ok'
TAKEN = 'taken'
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
        return raw_input('Enter your name:')

    def receive(self):
        return self.socket.recv(4096)

    def send(self, text):
        self.socket.sendall(text)

    def set(self, (keys, values)):
        dict = {}
        for i in range(len(keys)):
            dict[keys[i]] = values[i]
        message = {SET: dict}
        # print 'for testing: this was sent - {}'.format(message)
        self.send(json.dumps(message))
        return self.receive()
    COMMANDS[SET] = set

    def get(self, keys):
        message = {GET: keys}
        self.send(json.dumps(message))
        return self.receive()
        return self.receive()
    COMMANDS[GET] = get

    def search(self, str):
        message = {SEARCH: str}
        self.send(json.dumps(message))
        return self.receive()
        return self.receive()
    COMMANDS[SEARCH] = search

    def sendName(self, name):
        self.send(name)
        response = self.socket.receive()
        if response == TAKEN:
            print "name '{}' is already taken"
            return
        print 'name was accepted :)'

    def printCommandsList(self):
        for i in range(len(COMMANDS)):
            print '{}. {}'.format(i, COMMANDS.keys()[i])

    def enterCommand(self):
        self.printCommandsList()
        command_number = raw_input('Enter command number...')
        command_name = COMMANDS.keys()[command_number]
        client = COMMANDS[command_name]

        COMMANDS[command_number]()


    def sendCommand(self, command_name):



    def startConnection(self):
        self.connect()
        self.name = self.getName()
        self.sendName(self.name)
        self.sendCommand(self.enterCommand())



def main():
    c = Client(address = (IP, PORT))

    response = c.set((['first_key'],['first_value']))
    print json.loads(response)
    response = c.get('first_key')
    print json.loads(response)
    response = c.search('f')
    print json.loads(response)


if __name__ == "__main__":
    main()

