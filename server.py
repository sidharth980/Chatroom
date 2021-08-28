import socket
import threading

class Server():
    port = 5050
    # host = socket.gethostbyname(socket.gethostname())
    host = '0.0.0.0'
    # server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # server.bind((host,port))

    maxLength = 64
    messageFormat = 'utf-8'

    clients = []

    def __init__(self,host,port):
        self.port = port
        self.host = host
        self.startServer()

    def messageClient(self,msg,conection):
        print(f"sending : {msg}")
        for x in self.clients:
            if x !=conection:
                message = msg.encode(self.messageFormat)
                msg_length = len(message)
                send_length = str(msg_length).encode(self.messageFormat)
                send_length += b' ' * (self.maxLength - len(send_length))
                x.send(send_length)
                x.send(message)

    def clientHandler(self,conection,addr):
        print(f"{addr} has connected to server")
        self.clients.append(conection)
        name = conection.recv(1024).decode(self.messageFormat)
        link = True
        while link:
            messagelength = conection.recv(self.maxLength).decode(self.messageFormat)
            if messagelength:
                messagelength = int(messagelength)
                message = conection.recv(messagelength).decode(self.messageFormat)
                if message == "disc":
                    link = False
                else:
                    message = name + " : " + message
                    self.messageClient(message,conection)
            
    def work(self):
        self.server.listen()
        print("Server is listening")
        while True:
            connection,addr = self.server.accept()
            thread = threading.Thread(target=self.clientHandler,args=(connection,addr))
            thread.start()
            

    def startServer(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        print(f"Server Started \nAddress:{self.host}\nPort:{self.port}")
        self.work()

newserver = Server(input("Enter Ip: "),int(input("Enter Port: ")))