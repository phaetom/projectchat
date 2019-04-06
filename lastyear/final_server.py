#Write a GUI based chat server program which can allow 5 clients (each client must
#be handled by threads in server, i.e. incoming traffic by one thread for each client
#and outgoing traffic another thread. ).
#
#• 1.Communication will be conducted over TCP.
#• 2.The client will initiate a chat session by creating a socket connection to the server.
#• 3.The server will accept the connection, listen for any messages from the client, and accept them.
#• 4.The client will listen on the connection for any messages from the server, and accept them.
#• 5.The server will send any messages from the client to all the other connected clients except the sending client.
#• 6.Messages will be encoded in the UTF-8 character set for transmission

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}
HOST = '0.0.0.0'
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM) 
SERVER.bind(ADDR)

def broadcast(msg, prefix=""):  # prefix is for name identification. for broadcasting as the name says
    for sock in clients:
        sock.send(bytes(prefix)+msg)
        #sock.send(bytes(prefix, "utf8")+msg)


def accept_incoming_connections(): # deals with handling of incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        intro = bytes("Hello! You are all set to start chatting! Please enter you name first:")
        client.send(intro.encode('utf-8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf-8")
    welcome = bytes('Welcome %s! If you ever want to quit, type {quit} to exit.' % name)
    client.send(welcome.encode("utf-8"))
    msg = bytes("%s has joined the chat!" % name) #lets others know that user has joined or left
    broadcast(msg.encode("utf-8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name)) #lets others know that user has joined or left
            break
            
            
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections 
    print("Waiting for the users to connect...") #this is printed when program starts
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()






