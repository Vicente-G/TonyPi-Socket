import cv2
import time
import socket
import numpy as np
import torch

model = torch.hub.load(
    "ultralytics/yolov5", "custom",
    path="v5n.pt"
)

WIDTH, HEIGHT = 256, 144
ACTIONS = {
    "hola": b"wave",
}

def check_substring(arr, word):
    counter, n = 0, len(arr) - 1
    for char in arr:
        if char == word[min(counter, n)]:
            counter += 1
    return counter >= len(word)

def check(arr):
    if len(arr) < 2:
        return None
    for word in ACTIONS.keys():
        if check_substring(arr, word):
            return word
    return None

def add_text(img, detections, selected):
    counter = 0
    for idx, char in enumerate(detections):
        color = (0, 0, 255)
        if selected is not None and char == selected[counter]:
            counter += 1
            color = (0, 255, 0)
        pos, sz = ((idx + 1) * (WIDTH - 10) // 13, HEIGHT - 20), WIDTH // 240
        cv2.putText(img, char.upper(), pos, 0, sz, color, sz+1)

def main(server):
    conn, _ = server.accept()
    selected = None
    detections = []
    last_detection = None
    while True:
        data = conn.recv(100000000)
        im0 = cv2.imdecode(np.frombuffer(data, np.uint8), 1)
        if im0 is None:
            continue
        result, choice = model(im0[:, :, ::-1]), None
        print(result)
        if result.pred[0].tolist():
            choice = model.names[int(result.pred[0].tolist()[-1][-1])]
        if choice is not None and choice != last_detection:
            detections.append(choice)
            last_detection = choice
        elif choice is None:
            last_detection = None
        detections = detections[-12:]
        selected = check(detections)

        add_text(im0, detections, selected)
        cv2.imshow("Robot's view", im0)
        if cv2.waitKey(1) % 256 == 27: # pressing ESC
            conn.sendall(b"exit")
            break
        if selected is not None:
            conn.sendall(ACTIONS[selected])
            detections.clear()
            time.sleep(1)

    cv2.destroyAllWindows()
    conn.close()
    server.close()

if __name__ == "__main__":
    IP, PORT = "192.168.149.68", 30000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print("Server Ready!")
    main(server)
