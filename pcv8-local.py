import cv2
import socket
import numpy as np
import ultralytics

# Run: pdm run python3 pcv8-local.py

camera = cv2.VideoCapture(0)
model = ultralytics.YOLO("v8n.pt")
WIDTH, HEIGHT = 1280, 720
ACTIONS = {
    "hola": b"wave",
    "sumo": b"bow",
    "baila": b"twist",
    "squat": b"squat",
    "flex": b"sit_ups",
    "dio": b"chest",
    "bro": b"lift_down",
    "dab": b"left_uppercut",
    "rick": b"wing_chun",
    "cueca": b"stepping",
    "kpop": b"17",
    "rapear": b"20",
    "drama": b"22"
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
        pos, sz = ((idx + 1) * (WIDTH - 30) // 25, 80), WIDTH // 450
        cv2.putText(img, char.upper(), pos, 0, sz, color, sz+2)

def main(server):
    conn, _ = server.accept()
    selected = None
    detections = []
    last_detection = None
    while True:
        ret, im0 = camera.read()
        if not ret:
            continue
        result = model.predict(im0, device="cpu", conf=0.5)[0]
        classes = result.boxes.cls.numpy().flatten().tolist()
        if classes and result.names[classes[0]] != last_detection:
            detections.append(result.names[classes[0]])
            last_detection = result.names[classes[0]]
        elif not classes:
            last_detection = None
        detections = detections[-24:]
        selected = check(detections)

        display = result.plot()
        add_text(display, detections, selected)
        cv2.imshow("Robot's view", display)
        if cv2.waitKey(1) % 256 == 27: # pressing ESC
            conn.sendall(b"exit")
            break
        if selected is not None:
            conn.sendall(ACTIONS[selected])
            detections.clear()
            conn.recv(1000)

    cv2.destroyAllWindows()
    camera.release()
    server.close()

if __name__ == "__main__":
    IP, PORT = "192.168.149.213", 30000
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print("Server Ready!")
    main(server)
