#import numpy as np #Required for extraction
# Libraries for selecting a proper image to be used for extraction
from PIL import Image
import cv2 #For computer Vision
from picamera import PiCamera
from time import sleep

# Libraries for selecting a proper image to be used for FireBase
from datetime import datetime
from firebase import firebase

#Libraries for selecting a proper image to be used for Fingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import hashlib

#Libraries for selecting a proper image to be used for Cloud Vision
import pyrebase
import os,io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd

#Libraries for selecting a proper image to be used for GPS
import Neo6mGPS


def rotate(img):
    (h, w) = img.shape[:2] # get image height, width
    center = (w / 2, h / 2) # calculate the center of the image

    angle270 = 270
    scale = 1.0
     
    M = cv2.getRotationMatrix2D(center, angle270, scale) # Perform the counter clockwise rotation holding at the center 270 degrees
    
    rotated270 = cv2.warpAffine(img, M, (w,h))
    
    (h, w) = img.shape[:2] # get image height, width
    center = (w / 2, h / 2) # calculate the center of the image
    angle270 = 87
    M = cv2.getRotationMatrix2D(center, angle270, scale)
    rotated270 = cv2.warpAffine(img, M, (w,h))
    #print("Rotate")
    return(rotated270)

def getDl(addr):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/pi/Desktop/gocr/vehicleauth2020-ba6fcbac0899.json"
    client=vision.ImageAnnotatorClient()
    filePath='/home/pi/Desktop/Running/rotated_image.jpg'

    with io.open(filePath,'rb') as image_file:
        content=image_file.read()

    image = vision.types.Image(content=content)
    response=client.text_detection(image=image)
    texts = response.text_annotations

    df=pd.DataFrame(columns=['locale','description'])
    for text in texts:
        df=df.append(
            dict(
                locale=text.locale,
                description=text.description
                ),
            ignore_index=True
            )
    #print(df)
    for i in range(len(df)):
        if df['description'][i] == 'No':
            dl=df['description'][i+1]+" "+df['description'][i+2]
            #print(dl)
            return(dl)
            break
        


def location(ref,linkVehicleDriverLoc,c):
    cordi=Neo6mGPS.start()

    if cordi[0]!=0:
        ref.put(linkVehicleDriverLoc,'Lat',lat)
    if cordi[1]!=0:
        ref.put(linkVehicleDriverLoc,'Long',long)
    
    
def checkStaus(ref):
    linkVehicleStatus="https://proj-db-c86ba.firebaseio.com/LMV/9983/Status/-LzfQyXGdcKken1Wfnvt/value"
    stat=ref.get(linkVehicleStatus,'')
    if stat==1:
        return (True)
    else:
        return (False)
    
def vehiType(ref,vehicleType,universalLoc):
    vehicleTypeLoc=universalLoc+vehicleType
    vehiT=ref.get(vehicleTypeLoc,'')
    if vehiT == 1:
        return (True)
    else:
        return (False)
    
def putData(ref,linkVehicleData,driverName,driverLastName,succ,sco,DLNO):
    if succ==1:
        val = True
    else:
        val = False
    data={
        'Name':driverName,
        'LastName': driverLastName,
        'Success': val,
        'biom':sco,
        'LicenseNo':DLNO,
        'Lat':0,
        'Long':0
        #insert timestamp if you want to
        }
    driverBucketId=ref.post(linkVehicleData,data)
    return(driverBucketId)

def getID(driverBucketId):
    locId=list(str(driverBucketId))
    count=-1
    flag=0
    locMainId=""

    for i in range (len(locId)):
        if flag == 0:
            if locId[i]==":":
                count=2
                continue
            
            if count>0 :
                #print(i)
                count-=1
                flag=0
            elif count==0 and flag==0:
                if locId[i] !="'":
                    locMainId=locMainId+locId[i]
                else:
                    break
            else:
                continue
            
    return (locMainId)

def changeStat(ref,val):
    linkVehicleStatus="https://proj-db-c86ba.firebaseio.com/LMV/9983/Status/-LzfQyXGdcKken1Wfnvt"
    refrence.put(linkVehicleStatus,'value',0)
    
def checkAuth():
## Search for a finger
##

## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

## Gets some sensor information
    #print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Searchs template
        result = f.searchTemplate()
        scan=f.downloadCharacteristics(0x01)
        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            return (False , scan)
            exit(0)
        else:
            print("Match Found")
           # print('Found template at position #' + str(positionNumber))
           # print('The accuracy score is: ' + str(accuracyScore))
            return (True , scan)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)


    
def fingerprintGrab(ref,bucketLoc,universalLoc):
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)

## Gets some sensor information
   # print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    link=universalLoc+'biom'
## Tries to search the finger and calculate hash
    try:
        f.deleteTemplate(0)
        char=ref.get(link,'')
        f.uploadCharacteristics(0x02,char)
        f.createTemplate()
        positionNumber = f.storeTemplate()
        auth, scan=checkAuth()
        return (auth, scan)
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
    
def fetching(DLNO, productId, vehicleType, ref):
    drivingLicenseBucketId=ref.get('/DrivingLicense/details','')
    flag=0
    passCount=0
    drivingLicenseBucketName=list(drivingLicenseBucketId)
    #print(type(DLNO)) #DLN type str
    for search in drivingLicenseBucketName:
        sign=0
        loc='/DrivingLicense/details/'+search+'/LicenseNo'
        resultDLNO=ref.get(loc,'')
        if resultDLNO == DLNO:
            flag=1
            bucketLoc=search
            break
    if flag==1:
        universalLoc='/DrivingLicense/details/'+bucketLoc+'/'
        nameLoc=universalLoc+'Name'
        lastNameLoc=universalLoc+'LastName'
        linkVehicleData=vehicleType+"/"+productId
        driverName=ref.get(nameLoc,'')
        driverLastName=ref.get(lastNameLoc,'')
        
#         vehicleTypeLoc=universalLoc+vehicleType
        if vehiType(ref,vehicleType,universalLoc):
            #passwordLoc=universalLoc+'Pwd'
            #password=ref.get(passwordLoc,'')
            #linkVehicleStatus="https://proj-db-c86ba.firebaseio.com/LMV/9983/Status/-LzfQyXGdcKken1Wfnvt/value"
            if checkStaus(ref):
                checkA, sco=fingerprintGrab(ref,bucketLoc,universalLoc)
                
                
                
                if checkA:
                #if 1 == 1 :#add stats check
                    print("Yeet!")
                    sign=1
                    succ=1
                    
                    driverBucketId=putData(ref,linkVehicleData,driverName,driverLastName,succ,sco,DLNO)#put values
                    
                    locMainId= getID(driverBucketId)
                    #print(locMainId)
                    linkVehicleDriverLoc=linkVehicleData+'/'+locMainId
                    #print(linkVehicleDriverLoc)
                    location(ref,linkVehicleDriverLoc,0)
                    
                else:
                    while True:
                        print("Passwords did not match for ", passCount+1)
                        if passCount <3:
                            checkA, sco=checkAuth()
                            if checkA :
                                succ=1
                                driverBucketId=putData(ref,linkVehicleData,driverName,driverLastName,succ,sco,DLNO)#put values
                                locMainId= getID(driverBucketId)
                                #print(locMainId)
                                linkVehicleDriverLoc=linkVehicleData+'/'+locMainId
                                #print(linkVehicleDriverLoc)
                                location(ref,linkVehicleDriverLoc,0)
                                sign=1
                                break
                            else:
                                passCount+=1
                        else:
                            succ=0
                            driverBucketId=putData(ref,linkVehicleData,driverName,driverLastName,succ,sco,DLNO)#put values
                            val=0
                            changeStat(ref,val)
                            print("Oops!!! Changing status request owner to change it back")
                            
                            break
                        
                    locMainId= getID(driverBucketId)
                    linkVehicleDriverLoc=linkVehicleData+'/'+locMainId
                    location(ref,linkVehicleDriverLoc,0)
                    
            else:
                print("Vehicle locked by owner.")
        else:
            print("You are not allowed to drive the vehicle.")
    else:
        print("Sorry no records found!!!")
    if sign ==1:
        return(linkVehicleDriverLoc)
    else:
        return(sign)
camera = PiCamera()
camera.capture('/home/pi/Desktop/Running/image100.jpg')
img = cv2.imread('image100.jpg')
#print("Taken")
#************************************Calling the function to rotate and displaying/storing the image with the same name************ 
rotateImage=rotate(img)
cv2.imwrite('rotated_image.jpg',rotateImage)
#************************************End of rotation*********************************************


addr='/home/pi/Desktop/Running/rotated_image.jpg'
dno=getDl(addr)
print(dno)


pid='9983'
vtyp='LMV'
fbLink="https://proj-db-c86ba.firebaseio.com"
#try:
refrence=firebase.FirebaseApplication(fbLink, None)
locUpdate=fetching(dno, pid, vtyp, refrence)
if locUpdate !=0:
    statLink=vtyp+"/"+pid+"/Status/-LzfQyXGdcKken1Wfnvt/loc"
    c=0
    while(refrence.get(statLink,'')==1):
        c+=1
        location(refrence,locUpdate,c)
        time.sleep(10)
#except:
    
 #   if dno==primary:
  #      print("Connection failed.....Owner driving......Access allowed")

   # else:
    #    print("Here")
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image