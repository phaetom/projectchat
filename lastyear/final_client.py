#• 1.Communication will be conducted over TCP.
#• 2.The client will initiate a chat session by creating a socket connection to the server.
#• 3.The server will accept the connection, listen for any messages from the client, and accept them.
#• 4.The client will listen on the connection for any messages from the server, and accept them.
#• 5.The server will send any messages from the client to all the other connected clients except the sending client.
#• 6.Messages will be encoded in the UTF-8 character set for transmission

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive(): #to deal with receiving messages
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # when possibly client has left the chat.
            break


def send(event=None):  # handles sending. event is passed by binders.
    msg = textbox.get()
    textbox.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None): #to close the program
    textbox.set("{quit}")
    send()



top = tkinter.Tk() #creates the frame. rename top to something else
top.title("Pyhton class chat") 

messages_frame = tkinter.Frame(top)
textbox = tkinter.StringVar()  # For the messages to be sent.
textbox.set("Start typing your message...") #prefilled text for user
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

msg_list = tkinter.Listbox(messages_frame, height=25, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH) #pack used instead of grid
#msg_list.pack()
messages_frame.pack()

typing_box = tkinter.Entry(top, textvariable=textbox)
typing_box.bind("<Return>", send) 
typing_box.pack(fill=tkinter.BOTH, padx=5) #using pack instead of grid to place items
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, ipady=20, expand=1)
send_button.config(background="yellow") #using pack instead of grid to place items
top.protocol("WM_DELETE_WINDOW", on_closing) #invokes the function for closing


HOST = '127.0.0.1'
PORT = 8000

#In case we need to ask for host input and port
#HOST = input('Enter host: ')
#PORT = input('Enter port: ')
#if not PORT:
#    PORT = 8000  # Default value.
#else:
#    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts the program