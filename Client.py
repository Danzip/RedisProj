import socket as s


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

def main():
    c=Client(address = ('127.0.0.1',3031))
    c.connect()
#     added line
# another line

if __name__ == "__main__":
    main()

