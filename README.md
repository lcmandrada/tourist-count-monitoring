# Tourist Count Monitoring

Facial Recognition for Tourist Count Monitoring Using Viola-Jones Algorithm for Intramuros Administration

The input of the system takes the form of motion, as detected by the PIR motion sensor, and image, as captured by the ArduCAM Mini OV5642 camera module. The prototype integrates the principles of sensor and vision-based systems for counting tourists to save on bandwidth and processing. It is implemented by taking an image only when motion is detected.

The input image is sent to the server on a local network through ESP8266 WiFi module for processing. The server with the python application employs Viola-Jones framework for face detection, Principal Component Analysis for face recognition, and Euclidean distance as parameter to be analyzed if the detected and recognized faces are of different tourists or not, without regard of the location where the face is taken. Only when the faces are different that the tourist count is incremented to ensure that the count only accounted for unique tourists.

# Build

It can be started by executing python3 on view.py.
```
python3 view.py
```

And it can be built by executing PyInstaller on view.spec.
```
pyinstaller view.spec
```

# Note

The input are sent to the tourist directory where detected and recognized faces are also saved.
Also, change the <directory> at view.spec to the folder containing the files.