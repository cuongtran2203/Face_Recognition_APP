import cv2
from .base_camera import BaseCamera
from coreAI.core_faceRECOG import *
from coreAI.create_db import create_user,face_detection
from coreAI.play_sound import *

class Camera(BaseCamera):
    def __init__(self):
        super().__init__()
        # self.play_sound=Sound()
        

    # over-wride of BaseCamera class frames method
    # @staticmethod
    def frames(self):
        camera = cv2.VideoCapture("rtsp://admin:ZTLBTF@192.168.1.21:554")
        model=Face_recognition(720,1280)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        count=0
        while True:
            # read current frame
            _, frame = camera.read()
            count+=1
           
            frame=cv2.resize(frame,(1280,720))
            if count%30==0:
                t1=time.time()
                model.run(frame)
                
                
                print("Time processed {}".format(time.time()-t1))
                FPS=1/(time.time()-t1)
                cv2.putText(frame,"FPS :{:.3f}".format(FPS),(10,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,25,120),1)
                print("FPS :{:.3f}".format(FPS))
            yield frame

class Camera_extract(BaseCamera):
    def __init__(self):
        super().__init__()
        

    # over-wride of BaseCamera class frames method
    # @staticmethod
    def frames(self):
        camera = cv2.VideoCapture("rtsp://admin:ZTLBTF@192.168.1.21:554")
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        count=0
        while True:
            # read current frame
            _, frame = camera.read()
            count+=1
            frame=cv2.resize(frame,(1280,720))
            t1=time.time()
            face_detection(frame)
            print("Time processed {}".format(time.time()-t1))
            FPS=1/(time.time()-t1)
            cv2.putText(frame,"FPS :{:.3f}".format(FPS),(10,20),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,25,120),1)
            print("FPS :{:.3f}".format(FPS))
            yield frame
        
