import socket
import termcolor

# CONSTANTS
SERVER = "192.168.1.78"
PORT = 5050
FORMAT = "utf-8"
HEADER = 64
DISCONNECT = "!DISCONNECT"
ADDR = (SERVER, PORT)

# create socket object
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)

    # send the length of the message in binary
    msg_len = len(message)
    send_msg_len = str(msg_len).encode(FORMAT)
    send_msg_len += b' ' * (HEADER - len(send_msg_len))
    client.send(send_msg_len)
    client.send(message)

send("test")