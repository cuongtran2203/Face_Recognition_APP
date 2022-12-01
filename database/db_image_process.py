import os 
import cv2 
from torch_mtcnn import detect_faces
from PIL import Image
from arcface import ArcFace
import numpy as np
import sys
import time

face_rec=ArcFace.ArcFace()
root="db_image"
list_labels=os.listdir(root)
for label in list_labels:
    emb1=[]
    label_path=os.path.join(root,label)
    img_labels=os.listdir(label_path)
    for img_p in img_labels:
        img_path=os.path.join(label_path,img_p)
        frame=cv2.imread(img_path)
        emb1.append(face_rec.calc_emb(frame))
        print("Load: {}".format(img_path))
    with open("db/"+label+".npy","wb") as f :
        np.save(f,emb1)

       