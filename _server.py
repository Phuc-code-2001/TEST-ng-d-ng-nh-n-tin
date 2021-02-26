import socket, threading

class server:

    def __init__(self):
        self.NAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.NAME)
        self.PORT = 8000
        self.ADDR = (self.HOST, self.PORT)
        self.FORMAT = "UTF-8"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.ADDR)
    
        self.clientList = {}

    
    def listen(self):
        print(f"Server({self.ADDR}) is listening...")
        self.socket.listen()
        while True:
            clientSocket, clientAddr = self.socket.accept()
            if clientSocket != None and clientAddr[0] not in self.clientList:
                newConnect = threading.Thread(target=self.clientHandler, args=(clientSocket, clientAddr))
                self.clientList[clientAddr[0]] = clientSocket
                newConnect.start()
                print(f"Count client active: {threading.activeCount() - 1}")
            
    def clientHandler(self, clientSocket, addr):
        print(f"New connection: {addr} ")
        while True:
            try:
                message = clientSocket.recv(1024).decode(self.FORMAT)
                if message != None:
                    print(message)
                    name, targetName, text = message.split("||")
                    targetHost = None
                    try:
                        targetHost = socket.gethostbyname(targetName)
                        if targetHost in self.clientList:
                            self.clientList[targetHost].send((name + ": " + text).encode(self.FORMAT))
                        else:
                            clientSocket.send((targetName + " is offline...").encode(self.FORMAT))
                    except :
                        clientSocket.send(f"Not found {targetName} !!!")
                        
            except:
                break
        print(f"Client {addr} disconnected...")
        self.clientList.pop(addr[0])
        
if __name__ == '__main__':
    myServer = server()
    myServer.listen()