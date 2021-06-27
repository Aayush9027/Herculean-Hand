import cv2
import time
import os
import handtrackingmodule as htm
import pyautogui
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
         
def mouse():
    wCam, hCam = 640, 480
    frameR = 100#frame reduction
    smoothening = 8
    pTime = 0
    plocX, plocY = 0, 0#previous locations of x and y
    clocX, clocY = 0, 0#current locations of x and y

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)#width
    cap.set(4, hCam)#height
    detector = htm.handDetector(detectionCon=0.60,maxHands=1)#only one hand at a time
    wScr, hScr = pyautogui.size()

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        # 2. Get the tip of the index and middle fingers
        if len(lmList) != 0:
            x1,y1 = lmList[8][1:]
            x2,y2 = lmList[12][1:]
            #print(x1, y1, x2, y2)

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            
            #in moving mouse it was easy to move mouse upwards but in downward direction it is tough so we are setting region
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
                
            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
                    
                # 5. Convert Coordinates as our cv window is 640*480 but my screen is full HD so have to convert it accordingly
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))#converting x coordinates
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))#converting y
                    
                # 6. Smoothen Values avoid fluctuations
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                    
                # 7. Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)#wscr-clocx for avoiding mirror inversion
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)#circle shows that we are in moving mode
                plocX, plocY = clocX, clocY
                    
            # 8. Both Index and middle fingers are up : Clicking Mode but only if both fingers are near to each other
            if fingers[1] == 1 and fingers[2] == 1:    
                    
                # 9. Find distance between fingers so that we can make sure fingers are together
                length, img, lineInfo = detector.findDistance(8, 12, img)
                #print(length)

                # 10. Click mouse if distance short
                if length < 25:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
            
        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
        
        # 12. Display
        cv2.imshow("Image", img)
        if cv2.waitKey(1)==27:
            break          
    cv2.destroyAllWindows()    
    main()    
      
def paint():

    overlayList=[]#list to store all the images

    brushThickness = 25
    eraserThickness = 100
    drawColor=(255,0,255)#setting purple color

    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)# defining canvas

    #images in header folder
    folderPath="Header"
    myList=os.listdir(folderPath)#getting all the images used in code
    #print(myList)
    for imPath in myList:#reading all the images from the folder
        image=cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)#inserting images one by one in the overlayList
    header=overlayList[0]#storing 1st image 
    cap=cv2.VideoCapture(0)
    cap.set(3,1280)#width
    cap.set(4,720)#height

    detector = htm.handDetector(detectionCon=0.50,maxHands=1)#making object

    while True:

        # 1. Import image
        success, img = cap.read()
        img=cv2.flip(img,1)#for neglecting mirror inversion
        
        # 2. Find Hand Landmarks
        img = detector.findHands(img)#using functions fo connecting landmarks
        lmList,bbox = detector.findPosition(img, draw=False)#using function to find specific landmark position,draw false means no circles on landmarks
        
        if len(lmList)!=0:
            #print(lmList)
            x1, y1 = lmList[8][1],lmList[8][2]# tip of index finger
            x2, y2 = lmList[12][1],lmList[12][2]# tip of middle finger
            
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            #print(fingers)

            # 4. If Selection Mode - Two finger are up
            if fingers[1] and fingers[2]:
                xp,yp=0,0
                #print("Selection Mode")
                #checking for click
                if y1 < 125:
                    if 250 < x1 < 450:#if i m clicking at purple brush
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:#if i m clicking at blue brush
                        header = overlayList[1]
                        drawColor = (255, 0, 0)
                    elif 800 < x1 < 950:#if i m clicking at green brush
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200:#if i m clicking at eraser
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)#selection mode is represented as rectangle


            # 5. If Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)#drawing mode is represented as circle
                #print("Drawing Mode")
                if xp == 0 and yp == 0:#initially xp and yp will be at 0,0 so it will draw a line from 0,0 to whichever point our tip is at
                    xp, yp = x1, y1 # so to avoid that we set xp=x1 and yp=y1
                #till now we are creating our drawing but it gets removed as everytime our frames are updating so we have to define our canvas where we can draw and show also
                
                #eraser
                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)#gonna draw lines from previous coodinates to new positions 
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp,yp=x1,y1 # giving values to xp,yp everytime 
            
            #merging two windows into one imgcanvas and img
        
        # 1 converting img to gray
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        
        # 2 converting into binary image and thn inverting
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)#on canvas all the region in which we drew is black and where it is black it is cosidered as white,it will create a mask
        
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)#converting again to gray bcoz we have to add in a RGB image i.e img
        
        #add original img with imgInv ,by doing this we get our drawing only in black color
        img = cv2.bitwise_and(img,imgInv)
        
        #add img and imgcanvas,by doing this we get colors on img
        img = cv2.bitwise_or(img,imgCanvas)


        #setting the header image
        img[0:125,0:1280]=header# on our frame we are setting our JPG image acc to H,W of jpg images

        cv2.imshow("Image", img)
        #cv2.imshow("Canvas", imgCanvas)
        #cv2.imshow("Inv", imgInv)
        if cv2.waitKey(1)==27:
            break          
    cv2.destroyAllWindows()    
    main()    

def vol(): 
    
    wCam,hCam=640,480
    devices = AudioUtilities.GetSpeakers()#initialization for using pycaw
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange=volume.GetVolumeRange()
    minVol=volRange[0]#lower bound in range of values for volume in pycaw
    maxVol=volRange[1]#upper bound
    vol=0
    volbar=400
    volperc=0
    area=0
    colorVol=(255,0,0)
    PTime=0# previous time
    CTime=0# current time
    cap=cv2.VideoCapture(0)
    cap.set(3,wCam)
    cap.set(4,hCam) 
    detector=htm.handDetector(detectionCon=0.7,maxHands=1)
    while True:
        success,img=cap.read()#T or F,frame
        
        #find Hand
        img =detector.findHands(img)#using method built in my class
        lmlist,bbox=detector.findPosition(img,draw=True)#method for finding landmark
        if len(lmlist)!=0:#if hand is in front of camera thn only it can show points else none
            #print(lmlist[4],lmlist[8])# we want only thumb(4) and index finger(8) tip
            
            #filter based on size-bounding box
            area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100 #calculating area of box so that after a particular value only our gestures work
            #print(area)
            if 250<=area<=1300:

                #find distance beween index and thumb
                length,img,LineInfo=detector.findDistance(4,8,img)
                #print(length)

                #convert volume
                volbar=np.interp(length,[50,300],[400,150])
                volperc=np.interp(length,[50,300],[0,100])
            
                #smoothning
                smoothness=10
                volperc=smoothness*round(volperc/smoothness)

                #finger up
                fingers=detector.fingersUp()
                #print(fingers)

                #if pinky is down thn set volume
                if not fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volperc/100, None)#changing volume of our computer
                    cv2.circle(img,(LineInfo[4],LineInfo[5]),15,(0,255,0),cv2.FILLED)#gives button effect,changes color as we are setting volume                
                    colorVol=(0,255,0)
                else:
                    colorVol=(255,0,0)

        #drawings            
        cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
        cv2.rectangle(img,(50,int(volbar)),(85,400),(255,0,0),cv2.FILLED)     
        cv2.putText(img,f'{(int(volperc))}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        cVol=int(volume.GetMasterVolumeLevelScalar()*100)
        cv2.putText(img,f'Vol Set: {int(cVol)}%',(400,50),cv2.FONT_HERSHEY_COMPLEX,1,colorVol,3)
    
    #Frame rate
        CTime=time.time()#current time
        fps=1/(CTime-PTime)#FPS
        PTime=CTime#previous time is replaced by current time

        cv2.putText(img,f'FPS: {str(int(fps))}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)# showing Fps on screen
        

        cv2.imshow("Image",img)#showing img not imgRGB
        
        if cv2.waitKey(1)==27:
            break          
    cv2.destroyAllWindows()    
    main()    
              
def task_execution():

    wCam,hCam=640,480

    cap=cv2.VideoCapture(0)
    cap.set(3,wCam)
    cap.set(4,hCam)

    detector=htm.handDetector(detectionCon=0.70)
    totalFingers=0
    while True:

        success,img=cap.read()
        img=detector.findHands(img)
        lmList,bbox=detector.findPosition(img,draw=False)
        if len(lmList)!=0:
            fingers=detector.fingersUp()
            totalFingers = fingers.count(1)
            if(totalFingers==1):
                mouse() 
            elif(totalFingers==2):
                paint()
            elif(totalFingers==3):
                vol()                
        cv2.imshow("Image",img)
        cv2.waitKey(1)
                               
def main():
    print("INSTRUCTIONS-")
    print("A screen will be open once you type START")
    print("Show 1/2/3 Fingers according to numbering given to the tasks below")
    print("Tasks which you can perform-")
    print("1.AI Virtual Mouse")
    print("2.AI Virtual Paint")
    print("3.Gesture Volume control")
    print("Once you are doing a task the only way to end the task is by pressing Escape key")
    query=input("Type START to continue or EXIT to terminate: ")
    if "start" in query or "START" in query or "Start" in query:
        task_execution()
    else:
        exit()

if __name__=="__main__":
   main()