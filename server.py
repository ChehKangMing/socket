import socket
import threading
from unicodedata import name

# CONSTANTS
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
HEADER = 64
DISCONNECT = "!DISCONNECT"

EXISTING_USER_MSG = "[ERROR] Usernama already exist!"

# list of users
connected_users = {}


# create a new socket
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# bind server to IP ADDRESS and PORT
server.bind(ADDR)

# FUNCTIONS

def handle_client(conn, addr):
    username = register_user(conn, addr)

    print(f"[NEW CONNECTION] {addr} is now connected as {username}!")

    # while client is still connected
    connected = True
    while connected:

        # receive size of msg
        msg_len = conn.recv(HEADER).decode(FORMAT)
        
        # check if msg len is not null
        if msg_len:
            # parse msg_len to int
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if msg == DISCONNECT:
                connected = False
                print(f"[DISCONNECT] {username} is now disconnected!")
                del connected_users[username]
                print(connected_users)
                conn.close()
            else:
                print(f"[NEW MESSAGE] {username}: {msg}")


def register_user(conn, addr):
    name_len = conn.recv(HEADER).decode(FORMAT)
    if name_len:
        name_len = int(name_len)
        username = conn.recv(name_len).decode(FORMAT)

        if username in connected_users:
             conn.send("0".encode(FORMAT))
        else:
            conn.send("1".encode(FORMAT))
            connected_users[username] = addr
    print(connected_users.keys())
    return username
            


def start():
    # print starting msg
    print(f"[LISTENING] server is listening on {SERVER}")

    # server listen to incoming conections
    server.listen()

    # continue to listen until specified
    while True:
        # accept a connection
        # conn is a new socket object used to send/recv data
        # addr is addr of server
        conn, addr = server.accept()

        # create new thread for each individual new connecions
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        # start thread
        thread.start()

        # print active connections to server
        # active connections = total number of theads - 1, server.listen() will run on one thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

start()