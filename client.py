import socket

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

connected = True
unregistered = True

def send(msg):
    message = msg.encode(FORMAT)

    # send the length of the message in binary
    msg_len = len(message)
    send_msg_len = str(msg_len).encode(FORMAT)
    send_msg_len += b' ' * (HEADER - len(send_msg_len))
    client.send(send_msg_len)
    client.send(message)

def get_input():
    message = input("[INPUT] Enter Message (q to quit): ")
    if message == 'q':
        send(DISCONNECT)
        print("[DISCONNECT] Disconnected!")
        return False
    else:
        send(message)
    return True

def register_user():
    usrnme = input("[REGISTER] Enter username: ")
    username = usrnme.encode(FORMAT)
    name_len = len(username)
    send_name_len = str(name_len).encode(FORMAT)
    send_name_len += b' ' * (HEADER - len(send_name_len))
    client.send(send_name_len)
    client.send(username)

    registered_flag = client.recv(1).decode(FORMAT)
    if registered_flag == "1":
        print(f"[REGISTERED] Successfully registered as {usrnme}!")
        return False
    elif registered_flag == "0":
        print(f"[ERROR] {usrnme} already taken!")
        return True


while unregistered:
    unregistered = register_user()

while connected:
    connected = get_input()