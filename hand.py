import cv2
import time
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv2.VideoCapture(1)
mpHands=mp.solutions.hands
hands=mpHands.Hands(False)
mpDraw=mp.solutions.drawing_utils
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minv,maxv,curr=volume.GetVolumeRange()
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
            allHands=[]
            for handtype,handlms in zip(results.multi_handedness,results.multi_hand_landmarks):
                myHand={}
                lmList=[]
                xList=[]
                yList=[]
                for id,lm in enumerate(handlms.landmark):
                    h, w,c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([cx,cy])
                    xList.append(cx)
                    yList.append(cy)
                myHand["lmList"]=lmList
                if handtype.classification[0].label=="Right":
                    myHand["type"]="Left"
                else:
                    myHand["type"]="Right"
                allHands.append(myHand)
            if len(allHands)==2:
                time.sleep(0.5)
            else:  
                cv2.circle(img,((xList[8]+xList[4])//2,(yList[8]+yList[4])//2),12,(255,255,255),cv2.FILLED)
                l=math.hypot(xList[8]-xList[4],yList[8]-yList[4])
                cv2.line(img,(xList[8],yList[8]),(xList[4],yList[4]),(255,255,255),3)

                if l<40:#40 is the minimum value
                    cv2.circle(img,((xList[8]+xList[4])//2,(yList[8]+yList[4])//2),12,(0,0,255),cv2.FILLED)
                #max is 200 so range is 160 for minv to maxv.... so slope will be
                slope=(maxv-minv)/160
                x=(l-200)*slope
                if x>maxv:
                    x=maxv
                elif x<minv:
                    x=minv
                volume.SetMasterVolumeLevel(x,None)
    cv2.imshow("Image",img)
    cv2.waitKey(1)

