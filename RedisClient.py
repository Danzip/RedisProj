import socket as s
import json


SET = 'set'
GET = 'get'
SEARCH = 'search'
OK = 'ok'
TAKEN = 'taken'
UNKNOWN_COMMAND = 'unknown command'

class Client(object):
    def __init__(self, socket=None, address=('127.0.0.1', 3030)):
        if socket == None:
            socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket = socket
        self.address = address

    def log(self,text):
        print text

    def connect(self):
        self.socket.connect(self.address)
        self.log("connected to address {}".format(self.address))

    def receive(self):
        return self.socket.recv(4096)

    def send(self, text):
        self.socket.sendall(text)
        print ("'{}' message sent".format(text))

    def set(self, keys, values):
        dict = {}
        for i in range(len(keys)):
            dict[keys[i]] = values[i]
        message = {SET: dict}
        print 'for testing: this was sent - {}'.format(message)
        self.socket.sendall(json.dumps(message))
        return self.receive()

    def get(self, keys):
        message = {GET: keys}
        print 'for testing: this was sent - {}'.format(message)
        self.socket.sendall(json.dumps(message))
        return self.receive()

    def search(self, str):
        message = {SEARCH: str}
        print 'for testing: this was sent - {}'.format(message)
        self.socket.sendall(json.dumps(message))
        return self.receive()


def main():
    c = Client(address = ('127.0.0.1',3030))
    c.connect()
#     added line
    response = c.receive()
    print "connected to server" # prints if got response
    name = 'gay'
    c.send(name) # sends my name
    response = c.receive()
    if response == TAKEN:
        print "the name '{}' is already taken"
        return
    response = c.set(['first_key'],['first_value'])
    print json.loads(response)
    response = c.get('first_key')
    print json.loads(response)
    response = c.search('f')
    print json.loads(response)


if __name__ == "__main__":
    main()

