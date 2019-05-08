import cv2
import numpy as np
import time
import copy
import os
import glob
import csv
import pandas as pd  
from pyfirmata import Arduino, util
import multiprocessing as mpr
from threading import Thread
from datetime import datetime
from kalman_filter import KalmanFilter
from tracker import Tracker
import time
from tkinter import *


TLG01 = 13
TLR01 = 12

TLG02 = 11
TLR02 = 10

TLG03 = 9
TLR03 = 8

TLG04 = 7
TLR04 = 6

DELAY_LEVEL4 = 10
DELAY_LEVEL3 = 6
DELAY_LEVEL2 = 3
DELAY_LEVEL1 = 1

#########################################
fields = ('CCTV01 VIDEO', 'CCTV02 VIDEO', 'CCTV03 VIDEO', 'CCTV04 VIDEO', 'ARDUINO PORT')
def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"road_traffic4.mp4")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

def monthly_payment(entries):
    cctv01 = entries['CCTV01 VIDEO'].get()
    cctv02 = entries['CCTV02 VIDEO'].get()
    cctv03 = entries['CCTV03 VIDEO'].get()
    cctv04 = entries['CCTV04 VIDEO'].get()
    Thread(target = videoProcess, args=(cctv01,)).start() #thread = threading.Thread(target=worker, args=(i,))
    Thread(target = videoProcess2, args=(cctv02,)).start()
    Thread(target = videoProcess3, args=(cctv03,)).start()
    Thread(target = videoProcess4, args=(cctv04,)).start()

    

#########################################


board = Arduino("COM11")

def congCounter01():
    data = pd.read_csv('carinfor.csv')  
    x = data['CCTV03'].value_counts().to_dict()
    return x.get('CCTV01')

def congCounter02():
    data = pd.read_csv('carinfor.csv')  
    x = data['CCTV03'].value_counts().to_dict()
    return x.get('CCTV02')

def congCounter03():
    data = pd.read_csv('carinfor.csv')  
    x = data['CCTV03'].value_counts().to_dict()
    return x.get('CCTV03')
    
def congCounter04():
    data = pd.read_csv('carinfor.csv')  
    x = data['CCTV03'].value_counts().to_dict()
    return x.get('CCTV04')
hash_code = {congCounter01() : 'CCTV01'  ,congCounter02() : 'CCTV02', congCounter03() : 'CCTV03',congCounter04() : 'CCTV04'}
trafficLight = [congCounter01(),congCounter02() ,congCounter03() , congCounter04()] 
trafficLight.sort(reverse = True)

def checkcongestion4():
    if hash_code[trafficLight[0]] == 'CCTV01':
        
        print('switch ON traffic light TLG01')
        board.digital[TLG01].write(1)
        
        ######################################
        
        print('switch OFF traffic light TLR01')
        board.digital[TLR01].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        #time delay
        time.sleep(DELAY_LEVEL4)
        
        
    elif hash_code[trafficLight[0]] == 'CCTV02':
        
        print('switch ON traffic light TLG02')
        board.digital[TLG02].write(1)
        
        ##################################################
        
        print('switch OFF traffic light TLR02')
        board.digital[TLR02].write(0)
        
        print('turn OFF TLRO4')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG01')
        board.digital[TLG01].write(1)
        
        print('turn OFF TLR01')
        board.digital[TLR01].write(0)
        
        ###############################################
        
        
        time.sleep(DELAY_LEVEL4)
        
    elif hash_code[trafficLight[0]] == 'CCTV03':
    
        print('switch ON traffic light TLG03')
        board.digital[TLG03].write(1)
        
        #############################################
        print('switch OFF traffic light TLR03')
        board.digital[TLR03].write(0)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        #DELAY
        time.sleep(DELAY_LEVEL4)
    
    elif hash_code[trafficLight[0]] == 'CCTV04':
    
        print('switch ON traffic light TLG04')
        board.digital[TLG04].write(1)
        
        ########################################
        
        print('switch OFF traffic light TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn ON TLG03')
        board.digital[TLG03].write(1)
        
        print('turn OFF TLR03')
        board.digital[TLR03].write(0)
        
        time.sleep(DELAY_LEVEL4)
    
    else:
        print('CLOCK CONTROL THE TRAFFIC LIGHT')
        
def checkcongestion3():
    if hash_code[trafficLight[1]] == 'CCTV01':
        print('switch ON traffic light TLG01')
        board.digital[TLG01].write(1)
        
        ###########################################
        
        print('switch OFF traffic light TLR01')
        board.digital[TLR01].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        time.sleep(DELAY_LEVEL3)
    elif hash_code[trafficLight[1]] == 'CCTV02':
        
        print('switch ON traffic light TLG02')
        board.digital[TLG02].write(1)
        
        ###############################################
        print('switch OFF traffic light TLR02')
        board.digital[TLR02].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG01')
        board.digital[TLG01].write(1)
        
        print('turn OFF TLR01')
        board.digital[TLR01].write(0)
        
        time.sleep(DELAY_LEVEL3)
    
    elif hash_code[trafficLight[1]] == 'CCTV03':
    
        print('switch ON traffic light TLG03')
        board.digital[TLG03].write(1)
        
        ###############################################
        print('switch OFF traffic light TLR03')
        board.digital[TLR03].write(0)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        time.sleep(DELAY_LEVEL3)
    
    elif hash_code[trafficLight[1]] == 'CCTV04':
    
        print('switch ON traffic light TLG04')
        board.digital[TLG04].write(1)
        
        #############################################
        print('switch OFF traffic light TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn ON TLG03')
        board.digital[TLG03].write(1)
        
        print('turn OFF TLR03')
        board.digital[TLR03].write(0)
        
        time.sleep(DELAY_LEVEL3)
    
    else:
        print('CLOCK CONTROL THE TRAFFIC LIGHT')
        
def checkcongestion2():
    if hash_code[trafficLight[2]] == 'CCTV01':
        print('switch ON traffic light TLG01')
        board.digital[TLG01].write(1)
        
        #############################################
        print('switch OFF traffic light TLR01')
        board.digital[TLR01].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
       
        time.sleep(DELAY_LEVEL2)
    elif hash_code[trafficLight[2]] == 'CCTV02':
        
        print('switch ON traffic light TLG02')
        board.digital[TLG02].write(1)
        
        #####################################################
        print('switch OFF traffic light TLR02')
        board.digital[TLR02].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG01')
        board.digital[TLG01].write(1)
        
        print('turn OFF TLR01')
        board.digital[TLR01].write(0)
        
        time.sleep(DELAY_LEVEL2)
    
    elif hash_code[trafficLight[2]] == 'CCTV03':
    
        print('switch ON traffic light TLG03')
        board.digital[TLG03].write(1)
        
        #############################################
        print('switch OFF traffic light TLR03')
        board.digital[TLR03].write(0)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        time.sleep(DELAY_LEVEL2)
    
    elif hash_code[trafficLight[2]] == 'CCTV04':
    
        print('switch ON traffic light TLG04')
        board.digital[TLG04].write(1)
        
        ###########################################
        print('switch OFF traffic light TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn ON TLG03')
        board.digital[TLG03].write(1)
        
        print('turn OFF TLR03')
        board.digital[TLR03].write(0)
        
        time.sleep(DELAY_LEVEL2)
    else:
        print('CLOCK CONTROL THE TRAFFIC LIGHT')

def checkcongestion1():
    if hash_code[trafficLight[3]] == 'CCTV01':
        print('switch ON traffic light TLG01')
        board.digital[TLG01].write(1)
        
        ######################################
        print('switch OFF traffic light TLR01')
        board.digital[TLR01].write(0)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        #less time delay
        time.sleep(DELAY_LEVEL1)
    elif hash_code[trafficLight[3]] == 'CCTV02':
        
        print('switch ON traffic light TLG02')
        board.digital[TLG02].write(1)
        
        #############################################
        print('switch OFF traffic light TLR02')
        board.digital[TLR02].write(0)
        
        print('turn OFF TLRO4')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        print('turn ON TLR03')
        board.digital[TLR03].write(1)
        
        print('turn OFF TLG03')
        board.digital[TLG03].write(0)
        
        print('turn ON TLG01')
        board.digital[TLG01].write(1)
        
        print('turn OFF TLR01')
        board.digital[TLR01].write(0)
        
        time.sleep(DELAY_LEVEL1)
    elif hash_code[trafficLight[3]] == 'CCTV03':
    
        print('switch ON traffic light TLG03')
        board.digital[TLG03].write(1)
        
        #######################################
        print('switch OFF traffic light TLR03')
        board.digital[TLR03].write(0)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn OFF TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLG04')
        board.digital[TLG04].write(1)
        
        time.sleep(DELAY_LEVEL1)
    
    elif hash_code[trafficLight[3]] == 'CCTV04':
    
        print('switch ON traffic light TLG04')
        board.digital[TLG04].write(1)
        
        ############################################
        print('switch OFF traffic light TLR04')
        board.digital[TLR04].write(0)
        
        print('turn ON TLR01')
        board.digital[TLR01].write(1)
        
        print('turn OFF TLG01')
        board.digital[TLG01].write(0)
        
        print('turn OFF TLR02')
        board.digital[TLR02].write(0)
        
        print('turn ON TLG02')
        board.digital[TLG02].write(1)
        
        print('turn ON TLG03')
        board.digital[TLG03].write(1)
        
        print('turn OFF TLR03')
        board.digital[TLR03].write(0)
        time.sleep(DELAY_LEVEL1)
    
    else:
        print('CLOCK CONTROL THE TRAFFIC LIGHT')

def combinationControl():
    checkcongestion4()
    checkcongestion3()
    checkcongestion2()
    checkcongestion1()
    
#write to csv
def write_csv(data):
    with open('carinfor.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)
        
def videoProcess(cctv01):
     # The one I first used for testing; after staring at it so much, I've grown attached to this road :3
    #the_og_base_url = 'http://wzmedia.dot.ca.gov:1935/D3/89_rampart.stream/'
    
    
    
    BASE_URL = 'http://wzmedia.dot.ca.gov:1935/D3/80_whitmore_grade.stream/'
    FPS = 30
    '''
        Distance to line in road: ~0.025 miles
    '''
    ROAD_DIST_MILES = 0.025

    '''
        Speed limit of urban freeways in California (50-65 MPH)
    '''
    HIGHWAY_SPEED_LIMIT = 65
    
    

    # Initial background subtractor and text font
    fgbg = cv2.createBackgroundSubtractorMOG2()
    font = cv2.FONT_HERSHEY_PLAIN

    centers = [] 

    # y-cooridinate for speed detection line
    Y_THRESH = 240

    blob_min_width_far = 6
    blob_min_height_far = 6

    blob_min_width_near = 18
    blob_min_height_near = 18

    frame_start_time = None

    # Create object tracker
    tracker = Tracker(80, 3, 2, 1)

    # Capture livestream
    #cap = cv2.VideoCapture (BASE_URL + 'playlist.m3u8')
    cap = cv2.VideoCapture (cctv01)##

    while True:
        centers = []
        frame_start_time = datetime.utcnow()
        ret, frame = cap.read() #
        #ret, frame2 = cap2.read()##
        #ret, frame3 = cap.read()
        #ret, frame4 = cap.read()

        orig_frame = copy.copy(frame)

        #  Draw line used for speed detection
        cv2.line(frame,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2) #
        #cv2.line(frame2,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame3,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame4,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)

        # Convert frame to grayscale and perform background subtraction
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY) #
        #gray = cv2.cvtColor (frame2, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame3, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame4, cv2.COLOR_BGR2GRAY)
        
        fgmask = fgbg.apply (gray)

        # Perform some Morphological operations to remove noise
        kernel = np.ones((4,4),np.uint8)
        kernel_dilate = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_dilate)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find centers of all detected objects
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if y > Y_THRESH:
                if w >= blob_min_width_near and h >= blob_min_height_near:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                if w >= blob_min_width_far and h >= blob_min_height_far:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if centers:
            tracker.update(centers)

            for vehicle in tracker.tracks:
                if len(vehicle.trace) > 1:
                    for j in range(len(vehicle.trace)-1):
                        # Draw trace line
                        x1 = vehicle.trace[j][0][0]
                        y1 = vehicle.trace[j][1][0]
                        x2 = vehicle.trace[j+1][0][0]
                        y2 = vehicle.trace[j+1][1][0]

                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2) #
                        #cv2.line(frame2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame3, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame4, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

                    try:
                        '''
                            TODO: account for load lag
                        '''

                        trace_i = len(vehicle.trace) - 1

                        trace_x = vehicle.trace[trace_i][0][0]
                        trace_y = vehicle.trace[trace_i][1][0]

                        # Check if tracked object has reached the speed detection line
                        if trace_y <= Y_THRESH + 5 and trace_y >= Y_THRESH - 5 and not vehicle.passed:
                            cv2.putText(frame, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA) #
                            #cv2.putText(frame2, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            vehicle.passed = True

                            load_lag = (datetime.utcnow() - frame_start_time).total_seconds()

                            time_dur = (datetime.utcnow() - vehicle.start_time).total_seconds() - load_lag
                            time_dur /= 60
                            time_dur /= 60

                            
                            vehicle.mph = ROAD_DIST_MILES / time_dur

                            # If calculated speed exceeds speed limit, save an image of speeding car
                            if vehicle.mph > HIGHWAY_SPEED_LIMIT:
                                
                                
                                print ('UH OH, CONGETION DETECTED!')
                                cv2.circle(orig_frame, (int(trace_x), int(trace_y)), 20, (0, 0, 255), 2)
                                cv2.putText(orig_frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                                cv2.imwrite('speeding_%s.png' % vehicle.track_id, orig_frame)
                                #speedingDataSaver('%s' % int(vehicle.mph),'%s' % vehicle.track_id)
                                for x in range(1):
                                    write_csv([int(vehicle.mph),vehicle.track_id,'CONGESTION-DETECTED','CCTV01'])
                                
                                print ('FILE SAVED!')
                                print ('ACTION')
                                combinationControl()
                            
                                
                               
                            

                    
                        if vehicle.passed:
                            # Display speed if available
                            cv2.putText(frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                        else:
                            # Otherwise, just show tracking id
                            cv2.putText(frame, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            
                    except:
                        pass

        # Display all images
        cv2.imshow ('CCTV01', frame)
        #cv2.imshow ('opening/dilation', dilation)
        #cv2.imshow ('background subtraction', fgmask)
        #cv2.imshow ('frame2', frame2)#
        #cv2.imshow ('frame3', frame3)#
        #cv2.imshow ('frame4', frame3)#
        # Quit when escape key pressed
        if cv2.waitKey(5) == 27:
            break

        # Sleep to keep video speed consistent
        time.sleep(1.0 / FPS)

    # Clean up
    cap.release()
    #cap2.release()
    cv2.destroyAllWindows()
    df.to_csv('traffic.csv', sep=',')

    # remove all speeding_*.png images created in runtime
    for file in glob.glob('speeding_*.png'):
        os.remove(file)
        
###################################################################################################################

def videoProcess2(cctv02):
         # The one I first used for testing; after staring at it so much, I've grown attached to this road :3
    #the_og_base_url = 'http://wzmedia.dot.ca.gov:1935/D3/89_rampart.stream/'

    BASE_URL = 'http://wzmedia.dot.ca.gov:1935/D3/80_whitmore_grade.stream/'


    FPS = 30
    '''
        Distance to line in road: ~0.025 miles
    '''
    ROAD_DIST_MILES = 0.025

    '''
        Speed limit of urban freeways in California (50-65 MPH)
    '''
    HIGHWAY_SPEED_LIMIT = 65
    
    

    # Initial background subtractor and text font
    fgbg = cv2.createBackgroundSubtractorMOG2()
    font = cv2.FONT_HERSHEY_PLAIN

    centers = [] 

    # y-cooridinate for speed detection line
    Y_THRESH = 240

    blob_min_width_far = 6
    blob_min_height_far = 6

    blob_min_width_near = 18
    blob_min_height_near = 18

    frame_start_time = None

    # Create object tracker
    tracker = Tracker(80, 3, 2, 1)

    # Capture livestream
    #cap = cv2.VideoCapture (BASE_URL + 'playlist.m3u8')
    cap = cv2.VideoCapture (cctv02)##

    while True:
        centers = []
        frame_start_time = datetime.utcnow()
        ret, frame = cap.read() #
        #ret, frame2 = cap2.read()##
        #ret, frame3 = cap.read()
        #ret, frame4 = cap.read()

        orig_frame = copy.copy(frame)

        #  Draw line used for speed detection
        cv2.line(frame,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2) #
        #cv2.line(frame2,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame3,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame4,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)

        # Convert frame to grayscale and perform background subtraction
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY) #
        #gray = cv2.cvtColor (frame2, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame3, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame4, cv2.COLOR_BGR2GRAY)
        
        fgmask = fgbg.apply (gray)

        # Perform some Morphological operations to remove noise
        kernel = np.ones((4,4),np.uint8)
        kernel_dilate = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_dilate)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find centers of all detected objects
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if y > Y_THRESH:
                if w >= blob_min_width_near and h >= blob_min_height_near:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                if w >= blob_min_width_far and h >= blob_min_height_far:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if centers:
            tracker.update(centers)

            for vehicle in tracker.tracks:
                if len(vehicle.trace) > 1:
                    for j in range(len(vehicle.trace)-1):
                        # Draw trace line
                        x1 = vehicle.trace[j][0][0]
                        y1 = vehicle.trace[j][1][0]
                        x2 = vehicle.trace[j+1][0][0]
                        y2 = vehicle.trace[j+1][1][0]

                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2) #
                        #cv2.line(frame2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame3, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame4, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

                    try:
                        '''
                            TODO: account for load lag
                        '''

                        trace_i = len(vehicle.trace) - 1

                        trace_x = vehicle.trace[trace_i][0][0]
                        trace_y = vehicle.trace[trace_i][1][0]

                        # Check if tracked object has reached the speed detection line
                        if trace_y <= Y_THRESH + 5 and trace_y >= Y_THRESH - 5 and not vehicle.passed:
                            cv2.putText(frame, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA) #
                            #cv2.putText(frame2, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            vehicle.passed = True

                            load_lag = (datetime.utcnow() - frame_start_time).total_seconds()

                            time_dur = (datetime.utcnow() - vehicle.start_time).total_seconds() - load_lag
                            time_dur /= 60
                            time_dur /= 60

                            
                            vehicle.mph = ROAD_DIST_MILES / time_dur

                            # If calculated speed exceeds speed limit, save an image of speeding car
                            if vehicle.mph > HIGHWAY_SPEED_LIMIT:
                                
                                
                                print ('UH OH, CONGETION DETECTED!')
                                cv2.circle(orig_frame, (int(trace_x), int(trace_y)), 20, (0, 0, 255), 2)
                                cv2.putText(orig_frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                                cv2.imwrite('speeding_%s.png' % vehicle.track_id, orig_frame)
                                #speedingDataSaver('%s' % int(vehicle.mph),'%s' % vehicle.track_id)
                                for x in range(1):
                                    write_csv([int(vehicle.mph),vehicle.track_id,'CONGESTION-DETECTED','CCTV02'])
                                
                                print ('FILE SAVED!')
                                print ('ACTION')
                                combinationControl()
                            
                                
                               
                            

                    
                        if vehicle.passed:
                            # Display speed if available
                            cv2.putText(frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                        else:
                            # Otherwise, just show tracking id
                            cv2.putText(frame, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            
                    except:
                        pass

      
        # Display all images
        cv2.imshow ('CCTV02', frame)
        #cv2.imshow ('opening/dilation', dilation)
        #cv2.imshow ('background subtraction', fgmask)
        #cv2.imshow ('frame2', frame2)#
        #cv2.imshow ('frame3', frame3)#
        #cv2.imshow ('frame4', frame3)#
        # Quit when escape key pressed
        if cv2.waitKey(5) == 27:
            break

        # Sleep to keep video speed consistent
        time.sleep(1.0 / FPS)

    # Clean up
    cap.release()
    #cap2.release()
    cv2.destroyAllWindows()
    df.to_csv('traffic.csv', sep=',')

    # remove all speeding_*.png images created in runtime
    for file in glob.glob('speeding_*.png'):
        os.remove(file)
 
###################################################################################################################
       
def videoProcess3(cctv03):
             # The one I first used for testing; after staring at it so much, I've grown attached to this road :3
    #the_og_base_url = 'http://wzmedia.dot.ca.gov:1935/D3/89_rampart.stream/'

    BASE_URL = 'http://wzmedia.dot.ca.gov:1935/D3/80_whitmore_grade.stream/'
    FPS = 30
    '''
        Distance to line in road: ~0.025 miles
    '''
    ROAD_DIST_MILES = 0.025

    '''
        Speed limit of urban freeways in California (50-65 MPH)
    '''
    HIGHWAY_SPEED_LIMIT = 65
    
    

    # Initial background subtractor and text font
    fgbg = cv2.createBackgroundSubtractorMOG2()
    font = cv2.FONT_HERSHEY_PLAIN

    centers = [] 

    # y-cooridinate for speed detection line
    Y_THRESH = 240

    blob_min_width_far = 6
    blob_min_height_far = 6

    blob_min_width_near = 18
    blob_min_height_near = 18

    frame_start_time = None

    # Create object tracker
    tracker = Tracker(80, 3, 2, 1)

    # Capture livestream
    #cap = cv2.VideoCapture (BASE_URL + 'playlist.m3u8')
    cap = cv2.VideoCapture (cctv03)##

    while True:
        centers = []
        frame_start_time = datetime.utcnow()
        ret, frame = cap.read() #
        #ret, frame2 = cap2.read()##
        #ret, frame3 = cap.read()
        #ret, frame4 = cap.read()

        orig_frame = copy.copy(frame)

        #  Draw line used for speed detection
        cv2.line(frame,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2) #
        #cv2.line(frame2,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame3,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame4,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)

        # Convert frame to grayscale and perform background subtraction
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY) #
        #gray = cv2.cvtColor (frame2, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame3, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame4, cv2.COLOR_BGR2GRAY)
        
        fgmask = fgbg.apply (gray)

        # Perform some Morphological operations to remove noise
        kernel = np.ones((4,4),np.uint8)
        kernel_dilate = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_dilate)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find centers of all detected objects
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if y > Y_THRESH:
                if w >= blob_min_width_near and h >= blob_min_height_near:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                if w >= blob_min_width_far and h >= blob_min_height_far:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if centers:
            tracker.update(centers)

            for vehicle in tracker.tracks:
                if len(vehicle.trace) > 1:
                    for j in range(len(vehicle.trace)-1):
                        # Draw trace line
                        x1 = vehicle.trace[j][0][0]
                        y1 = vehicle.trace[j][1][0]
                        x2 = vehicle.trace[j+1][0][0]
                        y2 = vehicle.trace[j+1][1][0]

                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2) #
                        #cv2.line(frame2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame3, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame4, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

                    try:
                        '''
                            TODO: account for load lag
                        '''

                        trace_i = len(vehicle.trace) - 1

                        trace_x = vehicle.trace[trace_i][0][0]
                        trace_y = vehicle.trace[trace_i][1][0]

                        # Check if tracked object has reached the speed detection line
                        if trace_y <= Y_THRESH + 5 and trace_y >= Y_THRESH - 5 and not vehicle.passed:
                            cv2.putText(frame, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA) #
                            #cv2.putText(frame2, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            vehicle.passed = True

                            load_lag = (datetime.utcnow() - frame_start_time).total_seconds()

                            time_dur = (datetime.utcnow() - vehicle.start_time).total_seconds() - load_lag
                            time_dur /= 60
                            time_dur /= 60

                            
                            vehicle.mph = ROAD_DIST_MILES / time_dur

                            # If calculated speed exceeds speed limit, save an image of speeding car
                            if vehicle.mph > HIGHWAY_SPEED_LIMIT:
                                
                                
                                print ('UH OH, CONGETION DETECTED!')
                                cv2.circle(orig_frame, (int(trace_x), int(trace_y)), 20, (0, 0, 255), 2)
                                cv2.putText(orig_frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                                cv2.imwrite('speeding_%s.png' % vehicle.track_id, orig_frame)
                                #speedingDataSaver('%s' % int(vehicle.mph),'%s' % vehicle.track_id)
                                for x in range(1):
                                    write_csv([int(vehicle.mph),vehicle.track_id,'CONGESTION-DETECTED','CCTV03'])
                                
                                print ('FILE SAVED!')
                                print ('ACTION')
                                combinationControl()
                            
                                
                               
                            

                    
                        if vehicle.passed:
                            # Display speed if available
                            cv2.putText(frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                        else:
                            # Otherwise, just show tracking id
                            cv2.putText(frame, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            
                    except:
                        pass

   
        # Display all images
        cv2.imshow ('CCTV03', frame)
        #cv2.imshow ('opening/dilation', dilation)
        #cv2.imshow ('background subtraction', fgmask)
        #cv2.imshow ('frame2', frame2)#
        #cv2.imshow ('frame3', frame3)#
        #cv2.imshow ('frame4', frame3)#
        # Quit when escape key pressed
        if cv2.waitKey(5) == 27:
            break

        # Sleep to keep video speed consistent
        time.sleep(1.0 / FPS)

    # Clean up
    cap.release()
    #cap2.release()
    cv2.destroyAllWindows()
    df.to_csv('traffic.csv', sep=',')

    # remove all speeding_*.png images created in runtime
    for file in glob.glob('speeding_*.png'):
        os.remove(file)
 #########################################################################################################################       
def videoProcess4(cctv04):
                 # The one I first used for testing; after staring at it so much, I've grown attached to this road :3
    #the_og_base_url = 'http://wzmedia.dot.ca.gov:1935/D3/89_rampart.stream/'

    BASE_URL = 'http://wzmedia.dot.ca.gov:1935/D3/80_whitmore_grade.stream/'
    FPS = 30
    '''
        Distance to line in road: ~0.025 miles
    '''
    ROAD_DIST_MILES = 0.025

    '''
        Speed limit of urban freeways in California (50-65 MPH)
    '''
    HIGHWAY_SPEED_LIMIT = 65
    
    

    # Initial background subtractor and text font
    fgbg = cv2.createBackgroundSubtractorMOG2()
    font = cv2.FONT_HERSHEY_PLAIN

    centers = [] 

    # y-cooridinate for speed detection line
    Y_THRESH = 240

    blob_min_width_far = 6
    blob_min_height_far = 6

    blob_min_width_near = 18
    blob_min_height_near = 18

    frame_start_time = None

    # Create object tracker
    tracker = Tracker(80, 3, 2, 1)

    # Capture livestream
    #cap = cv2.VideoCapture (BASE_URL + 'playlist.m3u8')
    cap = cv2.VideoCapture (cctv04)##

    while True:
        centers = []
        frame_start_time = datetime.utcnow()
        ret, frame = cap.read() #
        #ret, frame2 = cap2.read()##
        #ret, frame3 = cap.read()
        #ret, frame4 = cap.read()

        orig_frame = copy.copy(frame)

        #  Draw line used for speed detection
        cv2.line(frame,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2) #
        #cv2.line(frame2,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame3,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)
        #cv2.line(frame4,(0, Y_THRESH),(640, Y_THRESH),(255,0,0),2)

        # Convert frame to grayscale and perform background subtraction
        gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY) #
        #gray = cv2.cvtColor (frame2, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame3, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor (frame4, cv2.COLOR_BGR2GRAY)
        
        fgmask = fgbg.apply (gray)

        # Perform some Morphological operations to remove noise
        kernel = np.ones((4,4),np.uint8)
        kernel_dilate = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        dilation = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel_dilate)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find centers of all detected objects
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if y > Y_THRESH:
                if w >= blob_min_width_near and h >= blob_min_height_near:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                if w >= blob_min_width_far and h >= blob_min_height_far:
                    center = np.array ([[x+w/2], [y+h/2]])
                    centers.append(np.round(center))

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #
                    #cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame3, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #cv2.rectangle(frame4, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if centers:
            tracker.update(centers)

            for vehicle in tracker.tracks:
                if len(vehicle.trace) > 1:
                    for j in range(len(vehicle.trace)-1):
                        # Draw trace line
                        x1 = vehicle.trace[j][0][0]
                        y1 = vehicle.trace[j][1][0]
                        x2 = vehicle.trace[j+1][0][0]
                        y2 = vehicle.trace[j+1][1][0]

                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2) #
                        #cv2.line(frame2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame3, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)
                        #cv2.line(frame4, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 255), 2)

                    try:
                        '''
                            TODO: account for load lag
                        '''

                        trace_i = len(vehicle.trace) - 1

                        trace_x = vehicle.trace[trace_i][0][0]
                        trace_y = vehicle.trace[trace_i][1][0]

                        # Check if tracked object has reached the speed detection line
                        if trace_y <= Y_THRESH + 5 and trace_y >= Y_THRESH - 5 and not vehicle.passed:
                            cv2.putText(frame, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA) #
                            #cv2.putText(frame2, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'I PASSED!', (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            vehicle.passed = True

                            load_lag = (datetime.utcnow() - frame_start_time).total_seconds()

                            time_dur = (datetime.utcnow() - vehicle.start_time).total_seconds() - load_lag
                            time_dur /= 60
                            time_dur /= 60

                            
                            vehicle.mph = ROAD_DIST_MILES / time_dur

                            # If calculated speed exceeds speed limit, save an image of speeding car
                            if vehicle.mph > HIGHWAY_SPEED_LIMIT:
                                
                                
                                print ('UH OH, CONGETION DETECTED!')
                                cv2.circle(orig_frame, (int(trace_x), int(trace_y)), 20, (0, 0, 255), 2)
                                cv2.putText(orig_frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                                cv2.imwrite('speeding_%s.png' % vehicle.track_id, orig_frame)
                                #speedingDataSaver('%s' % int(vehicle.mph),'%s' % vehicle.track_id)
                                for x in range(1):
                                    write_csv([int(vehicle.mph),vehicle.track_id,'CONGESTION-DETECTED','CCTV04'])
                                
                                print ('FILE SAVED!')
                                print ('ACTION')
                                combinationControl()
                            
                                
                               
                            

                    
                        if vehicle.passed:
                            # Display speed if available
                            cv2.putText(frame, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'MPH: %s' % int(vehicle.mph), (int(trace_x), int(trace_y)), font, 1, (0, 255, 255), 1, cv2.LINE_AA)
                        else:
                            # Otherwise, just show tracking id
                            cv2.putText(frame, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)#
                            #cv2.putText(frame2, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame3, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            #cv2.putText(frame4, 'ID: '+ str(vehicle.track_id), (int(trace_x), int(trace_y)), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                            
                    except:
                        pass
        # Display all images
        cv2.imshow ('CCTV04', frame)
        #cv2.imshow ('opening/dilation', dilation)
        #cv2.imshow ('background subtraction', fgmask)
        #cv2.imshow ('frame2', frame2)#
        #cv2.imshow ('frame3', frame3)#
        #cv2.imshow ('frame4', frame3)#
        # Quit when escape key pressed
        if cv2.waitKey(5) == 27:
            break

        # Sleep to keep video speed consistent
        time.sleep(1.0 / FPS)

    # Clean up
    cap.release()
    #cap2.release()
    cv2.destroyAllWindows()
    df.to_csv('traffic.csv', sep=',')

    # remove all speeding_*.png images created in runtime
    for file in glob.glob('speeding_*.png'):
        os.remove(file)
    

if __name__ == '__main__':
    #videoProcess()
    #Thread(target = videoProcess).start()
    #Thread(target = videoProcess2).start()
    #Thread(target = videoProcess3).start()
    #Thread(target = videoProcess4).start()
    #Thread(target = checkcongestion4).start()
    #Thread(target = checkcongestion3).start()
    #Thread(target = checkcongestion2).start()
    #Thread(target = checkcongestion1).start()
    #print('CCTV01:',congCounter01())
    #print('CCTV02:',congCounter02())
    #print('CCTV03:',congCounter03())
    #print('CCTV04:',congCounter04())
    #print(checkcongestion4())
    #print(checkcongestion3())
    #print(checkcongestion2())
    #print(checkcongestion1())
    #videoProcess4()
    #videoProcess3()
    #combinationControl()
    #Thread(target = combinationControl).start()
    
   root = Tk()
   root.title("SMART CITY INTELLIGENT TRAFFIC LIGHT CONTROL")
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b1 = Button(root, text = 'Start',
      command=(lambda e = ents: monthly_payment(e)))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   
   b2 = Button(root, text='Pause',
   command=(lambda e = ents: monthly_payment(e)))
   
   b2.pack(side = LEFT, padx = 5, pady = 5)
   
   b3 = Button(root, text = 'Quit', command = root.quit)
   b3.pack(side = LEFT, padx = 5, pady = 5)
   root.mainloop()


        
