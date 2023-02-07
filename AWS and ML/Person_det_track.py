#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""@author: ambakick
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
#from moviepy.editor import VideoFileClip
from collections import deque
from scipy.optimize import linear_sum_assignment as linear_assignment

import helpers
import detector
import tracker
import cv2
import requests
import pandas as pd


from urllib.request import urlopen
from bs4 import BeautifulSoup

# Global variables to be used by funcitons of VideoFileClop
frame_count = 0 # frame counter

max_age = 15  # no.of consecutive unmatched detection before 
             # a track is deleted

min_hits =1  # no. of consecutive matches needed to establish a track

tracker_list =[] # list for trackers
# list for track ID
track_id_list= deque(['1', '2', '3', '4', '5', '6', '7', '7', '8', '9', '10'])

debug = False

def assign_detections_to_trackers(trackers, detections, iou_thrd = 0.3):
    '''
    From current list of trackers and new detections, output matched detections,
    unmatchted trackers, unmatched detections.
    '''    
    
    IOU_mat= np.zeros((len(trackers),len(detections)),dtype=np.float32)
    for t,trk in enumerate(trackers):
        #trk = convert_to_cv2bbox(trk) 
        for d,det in enumerate(detections):
         #   det = convert_to_cv2bbox(det)
            IOU_mat[t,d] = helpers.box_iou2(trk,det) 
    
    # Produces matches       
    # Solve the maximizing the sum of IOU assignment problem using the
    # Hungarian algorithm (also known as Munkres algorithm)
    
    matched_idx = linear_assignment(-IOU_mat)        

    unmatched_trackers, unmatched_detections = [], []
    for t,trk in enumerate(trackers):
        if(t not in matched_idx[:,0]):
            unmatched_trackers.append(t)

    for d, det in enumerate(detections):
        if(d not in matched_idx[:,1]):
            unmatched_detections.append(d)

    matches = []
   
    # For creating trackers we consider any detection with an 
    # overlap less than iou_thrd to signifiy the existence of 
    # an untracked object
    
    for m in matched_idx:
        if(IOU_mat[m[0],m[1]]<iou_thrd):
            unmatched_trackers.append(m[0])
            unmatched_detections.append(m[1])
        else:
            matches.append(m.reshape(1,2))
    
    if(len(matches)==0):
        matches = np.empty((0,2),dtype=int)
    else:
        matches = np.concatenate(matches,axis=0)
    
    return matches, np.array(unmatched_detections), np.array(unmatched_trackers)       
    


def pipeline(img):
    '''
    Pipeline function for detection and tracking
    '''
    global frame_count
    global tracker_list
    global max_age
    global min_hits
    global track_id_list
    global debug
    
    frame_count+=1
    
    img_dim = (img.shape[1], img.shape[0])
    z_box = det.get_localization(img) # measurement
    if debug:
       print('Frame:', frame_count)
       
    
if __name__ == "__main__":    
     

    det = detector.PersonDetector()
    if debug: # test on a sequence of images
        images = [plt.imread(file) for file in glob.glob('./test_images/*.jpg')]
        
        for i in range(len(images))[0:7]:
             image = images[i]
             image_box = pipeline(image)   
             plt.imshow(image_box)
             plt.show()
           
    else: # test on a video file.
        
        # start=time.time()
        # output = 'test_v7.mp4'
        # clip1 = VideoFileClip("project_video.mp4")#.subclip(4,49) # The first 8 seconds doesn't have any cars...
        # clip = clip1.fl_image(pipeline)
        # clip.write_videofile(output, audio=False)
        # end  = time.time()
        cap = cv2.VideoCapture("rtsp://admin:ZIMOGQ@192.168.137.145:554/Streaming/Channels/101")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 8.0, (640,480))

        while(True):
            
            ret, img = cap.read()
            #print(img)
            #cv2.imshow('ghanta camera chalega', img)
            np.asarray(img)
            new_img = pipeline(img)
            out.write(new_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print(round(end-start, 2), 'Seconds to finish')