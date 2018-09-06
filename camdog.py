import cv2
from align import detect_face
import tensorflow as tf
import imutils
import pyautogui
import time
from pynput.keyboard import Key, Controller
import ctypes

sess = tf.Session()
pnet, rnet, onet = detect_face.create_mtcnn(sess, 'align')
minsize = 20 #20  # minimum size of face
threshold = [0.6, 0.7, 0.7] #[0.6, 0.7, 0.7]  # three steps's threshold
factor = 0.709  #0.709  # scale factor
cap = cv2.VideoCapture(0)
time1 = 0
flag_desktop = False
flag_lock = False
time2 = 0
    
while (True):
    ret,frame=cap.read()
    if(ret):
        frame = imutils.resize(frame, width=180)
        if (frame.ndim==2):
            frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
        faces, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
        n_faces = faces.shape[0]
        # print("number of faces :"+str(n_faces))
        if n_faces > 1:
            print("1")
            if not flag_desktop:
                flag_desktop = True
                pyautogui.hotkey('ctrl','win','right')
            time1 = time.time()
        elif flag_desktop and n_faces == 1 and (time.time()-time1) >= 6:
            print("2")
            pyautogui.hotkey('ctrl','win','left')
            flag_desktop = False

        if n_faces > 0:
            # repeating
            flag_lock = False
            time2 = time.time()
        elif not flag_lock and n_faces == 0 and (time.time()-time2) >= 3:
            print("4")
            flag_lock = True
            ctypes.windll.user32.LockWorkStation()            

    time.sleep(0.1)

