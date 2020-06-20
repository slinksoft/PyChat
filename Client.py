import socket,pickle,os
from threading import Thread
import time
import sys
s = socket.socket() #define socket
# take parameters via console
if(len(sys.argv) < 3) :
		print('Usage : python Client.py hostip port')
		sys.exit()
HOST = sys.argv[1]
PORT = int(sys.argv[2])
global isDone
global servName
servName = "Not defined yet"
isDone = 0 #indication if client is ready to leave the server
username = "" #client's username definition
#thread to continuously receive messages from the server
def receive():
    while True:
        global isDone, servName
        #if client entered "/exit", break out of receive thread
        if isDone == 1:
            break
        try:
            data = s.recv(8192)
            data = pickle.loads(data)
        except:
            print("")
        print(data[-1]) #extract last message
        #get servername from last message for server information
        if isDone == 0:
            processName = data[-1].split('|')
            servName = processName[1]
def sendMessages():
    while True:
        global isDone, servName
        msg = input(">>")
        msg = msg.replace('|', "")
        if not msg:
            print()
        elif msg == "/help":
            print("List of available commands:\n/info - Returns server information\n/exit - Leave the server")
        elif msg == "/info":
            print("Server Name:" + servName + "\nServer IP: " + HOST + "\nPort: " + str(PORT))
        elif msg == "/exit":
            isDone = 1
            #send message in bytes
            s.send(msg.encode())
            break
        else:
            #send message in bytes
            s.send(msg.encode())


        time.sleep(0.1)

#Attempt to connect to the server
def connect():
    print("Connecting...\n")
    try:
        s.connect((HOST, PORT))
    except:
        print("Unable to connect.")
        sys.exit()
    print("Successfully connected.")
    username = input("Enter your username: ")
    s.send(username.encode())
    Thread(target=receive).start()
    time.sleep(0.1)
    sendMessages()
    sys.exit(0)
connect()