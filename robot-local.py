import hiwonder.ActionGroupControl as AGC
import socket

CONNECTED = True
IP, PORT = "192.168.149.68", 30000
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.connect((IP, PORT))

def receive_actions():
    global CONNECTED
    while CONNECTED:
        selected = skt.recv(4096).decode()
        if selected == 'exit':
            CONNECTED = False
        AGC.runActionGroup(selected)

if __name__ == "__main__":
    receive_actions()
    skt.close()
