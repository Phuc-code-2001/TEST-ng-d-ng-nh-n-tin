import socket, threading


class client:

    def __init__(self):

        self.NAME = socket.gethostname()
        self.SERVERHOST = "192.168.160.1"
        self.TARGETNAME = "DESKTOP-G30GCKJ"
        self.PORT = 8000
        self.ADDR = (self.SERVERHOST, self.PORT)
        self.FORMAT = "UTF-8"

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.ADDR)
            server_handler = threading.Thread(target=self.serverHandler)
            server_handler.start()
        except:
            print("Connect to server faild")

    def serverHandler(self):
        while True:
            try:
                message = self.socket.recv(1024).decode(self.FORMAT)
                if message != None:
                    print("\nResponse from server: " + message)
            except:
                break
        print("!DISCONNECTED")

    def start(self):
        print("Start sending message...")
        while True:
            message = self.NAME + "||" + self.TARGETNAME + "||" + input("Enter a message: ")
            self.socket.send(message.encode(self.FORMAT))

if __name__ == '__main__':
    client = client()
    client.start()