import hiwonder.ActionGroupControl as AGC
import socket
import time

CONNECTED = True
IP, PORT = "192.168.149.213", 30000
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.connect((IP, PORT))

def receive_actions():
    while True:
        selected = skt.recv(4096).decode()
        if selected == 'exit':
            break
        AGC.runActionGroup(selected)
        time.sleep(0.2)
        AGC.runActionGroup("stand_slow")
        time.sleep(0.2)
        skt.send(b"ready")


if __name__ == "__main__":
    receive_actions()
    skt.close()
