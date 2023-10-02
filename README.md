# TonyPi-Socket
This repository allows to connect by socket your computer to [TonyPi Hiwonder Robot](https://www.hiwonder.com/products/tonypi?variant=31753114681431)

## American Sign Language Recognition with TonyPi
Currently the repository is configured to run American Sign Language (ASL) recognition on the TonyPi robot, using your computer's camera and running a Yolov8 neural network on your computer. 
So the robot only responds to detections, it does not perform processing.

The system recognizes the static letters of the American alphabet, so it can detect the following signs:

<img width="600" alt="image" src="https://github.com/Vicente-G/TonyPi-Socket/assets/81656647/073411e3-f8c0-4a91-bb86-2df6c73d232a">

> Notice that the letters J and Z are not static so you are not able to recognize them.

Considering this, we can spell words with the detected signs, and in this way associate the detected words with some action that the robot performs. 
For this, we map a dictionary of the words associated with the actions that TonyPi can perform, according to its collection of actions that it can run with `hiwonder.ActionGroupControl`. 

This dictionary we can find it as `ACTIONS` on [pcv8-local.py](pcv8-local.py) file.

## Run ASL recognition
1. Clone the repository and go to the directory where is located.
```
git clone https://github.com/Vicente-G/TonyPi-Socket.git
cd TonyPi-Socket
```
2. In the repository directory, run the following command to install all the necessary dependencies.
```
pdm sync
```
4. Now, connect to TonyPi's Wi-Fi network
5. On console run `ipconfig` command on Windows or `ifconfig` on macOS, to get the IP to connect the socket. You need to find TonyPi's IP, which is an **IPv4 address** that the WiFi is connected to.

<img width="600" alt="image" src="https://github.com/Vicente-G/TonyPi-Socket/assets/81656647/167efbb5-a660-40c8-aa18-a6211e7abd4e">

6. Now, on the main section of the [pcv8-local.py](pcv8-local.py) file (which will run on your computer), change the IP address to the one you got before.
```
if __name__ == "__main__":
    IP, PORT = "192.168.149.213", 30000
```
Also change it on the [robot-local.py](robot-local.py) file (which will run on the TonyPi robot).

7. With the files configured, we will now control the robot remotely with VNC Viewer, which you can download from [here](https://www.realvnc.com/es/connect/download/viewer/). Because you are already connected to the robot's Wi-Fi, access to the robot's desktop should appear on VNC aplication.
   <img width="895" alt="image" src="https://github.com/Vicente-G/TonyPi-Socket/assets/81656647/e657fe91-6347-459f-b3b6-3ac4c5067e79">

8. Once inside, you must send your updated [robot-local.py](robot-local.py) file to the robot, as indicated in this [guide](https://help.realvnc.com/hc/en-us/articles/360002250477-Transferring-Files-Between-Computers-#sending-files-to-realvnc-server-0-1).
9. Finally, we can run the ASL recognition. For this, first run the following command in the repository directory of your computer:
```
pdm run python3 pcv8-local.py
```
Wait until you can see a message like this: `Server ready!`.

10. Now, run the [robot-local.py](robot-local.py) on the TonyPi desktop with the following command on the directory where you save the file.
```
python3 robot-local.py
```
And you should see a window with your webcam detecting sign language :)
