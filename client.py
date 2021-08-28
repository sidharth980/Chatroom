import socket
import threading

class Client():
    connection = False

    maxLength = 64
    msgFormat = 'utf-8'

    def __init__(self,addr,port):
        self.host = addr
        self.port = port
        self.connectServer()

    def connectServer(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((self.host,self.port))
        print(f"Succesfully connected to {self.host}")
        self.connection = True
    
    def sendname(self,name):
        self.client.send(name.encode(self.msgFormat))

    def send(self,msg):
        if self.connection:
            message = msg.encode(self.msgFormat)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.msgFormat)
            send_length += b' ' * (self.maxLength - len(send_length))
            self.client.send(send_length)
            self.client.send(message)
        
    def rcvServer(self):
        while True:
            messagelength = self.client.recv(self.maxLength).decode(self.msgFormat)
            if messagelength:
                messagelength = int(messagelength)
                message = self.client.recv(messagelength).decode(self.msgFormat)
                print(message)

newclient = Client(input("Enter Ip: "),int(input("Enter Port: ")))
thread = threading.Thread(target=newclient.rcvServer)
thread.start()
newclient.sendname(input("Enter Your Name (25 letters) :"))
while True:
    msg = input()
    if msg:
        newclient.send(msg)
    else:
        break