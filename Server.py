from socketserver import ThreadingTCPServer, BaseRequestHandler
from threading import Thread
import pickle,datetime,sys

global name
HOST = "127.0.0.1"
PORT = 2788
messages = []
temp = []
# Class handling distribution of messages
class Echo(BaseRequestHandler):

    #receives new clients and decodes client messages
    def handle(self):
        global name
        try:
            self.temp = []
            Thread(target=self.send).start() #start thread to broadcast messages to all clients
            self.username = self.request.recv(8192).decode() #get client username
            #server terminal reference
            print("Connection from from {}:{}".format(self.client_address[0],
                                                     self.client_address[1]))
            while True:
                msg = self.request.recv(8192) #read client message
                if msg.decode() == "/exit":
                    msg = "[{} {}]: {}".format(datetime.datetime.now().strftime("%H:%M:%S"), " @ |" + name + "|",
                                   self.username + " has left the server.")
                    self.finish()
                else:
                    msg = "[{} {}]: {}".format(datetime.datetime.now().strftime("%H:%M:%S"),
                                   self.username + " @ |" + name + "|",
                                   msg.decode())

                messages.append(msg) #add to messages to send
                # Server terminal reference
                print(self.username + " to broadcast: " + msg)

                if not msg:
                    break
        except:
            print("client disconnected")
    #broadcast messages to all clients
    def send(self):

        global temp, messages
        while 1:
            if len(self.temp) != len(messages):
                data_string = pickle.dumps(messages)
                self.request.send(data_string)
                self.temp = [item for item in messages]

#start server
def startServer():
    global name
    # take parameters via console
    if (len(sys.argv) < 4):
        print('Usage : python Server.py Chatname hostip port')
        sys.exit()
    name = sys.argv[1]
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    name = name.replace('|', "")
    print("Server started on " + str(HOST) + "; listening on " + str(PORT) + "...")
    serv = ThreadingTCPServer((HOST,PORT), Echo)
    serv.serve_forever()
startServer()