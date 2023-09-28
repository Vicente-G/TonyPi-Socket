import threading
import socket
import cv2

CONNECTED = True
IP, PORT = "192.168.149.68", 30000
mutex = threading.Lock()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.connect((IP, PORT))

ACTIONS = {
    b"wave": lambda: print("Hello World!"),
}

def send_video():
    global CONNECTED
    while CONNECTED and cap.isOpened():
        ret, frame = cap.read()
        if ret: 
            _, jpeg = cv2.imencode('.jpg', frame)
            mutex.acquire()
            try:
                skt.sendall(jpeg.tobytes())
            except BrokenPipeError:
                CONNECTED = False
            mutex.release()

def receive_actions():
    global CONNECTED
    while CONNECTED:
        selected = skt.recv(4096)
        mutex.acquire()
        if selected == b'exit':
            CONNECTED = False
        elif selected in ACTIONS.keys():
            ACTIONS[selected]()
        mutex.release()

if __name__ == "__main__":
    send_video_thread = threading.Thread(target=send_video)
    send_video_thread.start()
    receive_actions()
    send_video_thread.join()
    skt.close()
    cap.release()
