import sys
import os
import json
from datetime import datetime

# #region agent log
log_path = '/Users/somansinghal/Downloads/car detection/.cursor/debug.log'
def log_debug(location, message, data, hypothesis_id=None):
    try:
        with open(log_path, 'a') as f:
            log_entry = {
                'sessionId': 'debug-session',
                'runId': 'post-fix',
                'hypothesisId': hypothesis_id,
                'location': location,
                'message': message,
                'data': data,
                'timestamp': int(datetime.now().timestamp() * 1000)
            }
            f.write(json.dumps(log_entry) + '\n')
    except:
        pass
# #endregion

# #region agent log
log_debug('Main_Webcam.py:1', 'Script execution started', {
    'python_version': sys.version,
    'python_executable': sys.executable,
    'sys_path': sys.path,
    'cwd': os.getcwd()
}, 'A')
# #endregion

# #region agent log
log_debug('Main_Webcam.py:2', 'Before cv2 import attempt', {
    'sys_path_count': len(sys.path),
    'sys_path_sample': sys.path[:5] if len(sys.path) > 5 else sys.path
}, 'A')
# #endregion

try:
    # #region agent log
    log_debug('Main_Webcam.py:3', 'Attempting cv2 import', {}, 'A')
    # #endregion
    import cv2
    # #region agent log
    log_debug('Main_Webcam.py:4', 'cv2 import successful', {
        'cv2_version': cv2.__version__ if hasattr(cv2, '__version__') else 'unknown',
        'cv2_path': cv2.__file__ if hasattr(cv2, '__file__') else 'unknown'
    }, 'A')
    # #endregion
except ImportError as e:
    # #region agent log
    log_debug('Main_Webcam.py:5', 'cv2 import failed', {
        'error_type': type(e).__name__,
        'error_message': str(e),
        'sys_path': sys.path
    }, 'A')
    # #endregion
    raise

# #region agent log
log_debug('Main_Webcam.py:6', 'Before imutils import attempt', {}, 'B')
# #endregion

import imutils

# #region agent log
log_debug('Main_Webcam.py:7', 'imutils import successful', {
    'imutils_path': imutils.__file__ if hasattr(imutils, '__file__') else 'unknown'
}, 'B')
# #endregion

# Suppress OpenCV warnings by setting log level
cv2.setLogLevel(0)  # 0 = SILENT, 1 = ERROR, 2 = WARN, 3 = INFO, 4 = DEBUG

cascade_src = 'cars.xml' #load the XML alg

car_cascade = cv2.CascadeClassifier(cascade_src) 

# #region agent log
# Suppress OpenCV warnings during device detection by redirecting stderr
from contextlib import contextmanager

@contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr

with suppress_stderr():
    available_devices = []
    for i in range(5):
        test_cam = cv2.VideoCapture(i)
        if test_cam.isOpened():
            available_devices.append(i)
        test_cam.release()

log_debug('Main_Webcam.py:9', 'Available camera devices checked', {
    'available_devices': available_devices
}, 'C')
# #endregion

# Use first available device, or default to 0 if none found
camera_device = available_devices[0] if available_devices else 0

# #region agent log
log_debug('Main_Webcam.py:9a', 'Selected camera device', {
    'selected_device': camera_device,
    'available_devices': available_devices
}, 'C')
# #endregion

cam=cv2.VideoCapture(camera_device)

# #region agent log
log_debug('Main_Webcam.py:10', 'After camera initialization', {
    'is_opened': cam.isOpened(),
    'device_index': camera_device
}, 'C')
# #endregion

if not cam.isOpened():
    # #region agent log
    log_debug('Main_Webcam.py:10a', 'Camera failed to open, exiting', {
        'device_index': camera_device,
        'available_devices': available_devices
    }, 'C')
    # #endregion
    print(f"Error: Could not open camera device {camera_device}")
    print(f"Available devices: {available_devices if available_devices else 'None'}")
    exit(1)

while True:

    # #region agent log
    log_debug('Main_Webcam.py:11', 'Before cam.read()', {
        'is_opened': cam.isOpened()
    }, 'D')
    # #endregion
    
    _,img=cam.read()
    
    # #region agent log
    log_debug('Main_Webcam.py:12', 'After cam.read()', {
        'img_is_none': img is None,
        'img_type': type(img).__name__ if img is not None else 'None',
        'img_shape': img.shape if img is not None else None
    }, 'D')
    # #endregion
    
    if img is None:
        # #region agent log
        log_debug('Main_Webcam.py:13', 'Image is None, skipping frame', {}, 'D')
        # #endregion
        continue
    
    # #region agent log
    log_debug('Main_Webcam.py:14', 'Before imutils.resize', {
        'img_shape_before': img.shape if img is not None else None
    }, 'D')
    # #endregion
    
    img=imutils.resize(img,width=500)
    
    # #region agent log
    log_debug('Main_Webcam.py:15', 'After imutils.resize', {
        'img_shape_after': img.shape if img is not None else None
    }, 'D')
    # #endregion  
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)  
    
    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),10) 
        
    cv2.imshow("Frame", img)   
    
    b=str(len(cars))
    a= int(b)
    n=a
    print("------------------------------------------------")
    print ("North: %d "%(n))
    if n>=8:
        print ("North More Traffic, Please on the RED Signal")
    else:
        print ("no traffic")
    if cv2.waitKey(33) == 27:
        break

cam.release()
cv2.destroyAllWindows()

