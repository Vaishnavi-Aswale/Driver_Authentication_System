import serial
import pynmea2

def calcDeg(cordi):
    cdi=""
    sec=""
    dec=-1
    
    decDeg=0
    decMint=0
    decSec=0.0
    final=0
    
    listCordi=list(cordi)
    for i in range(len(listCordi)):
        if listCordi[i] != '.':
            cdi=cdi+listCordi[i]
        else:
            dec=i
            break
    for i in range (dec+1,len(listCordi)):
        sec=sec+listCordi[i]
        
    deg=cdi[:-2]
    mint=cdi[-2:]
    
    listDeg=list(deg)
    listMint=list(mint)
    listSec=list(sec)
    
    for num in listDeg:
        decDeg=decDeg*10+int(num)
    
    for num in listMint:
        decMint=decMint*10+int(num)
        
    for i in range(len(listSec)-1,-1,-1):
        decSec=decSec/10+int(listSec[i])/10
    decMint+=decSec
    #print(decSec)
        
    final=decDeg+(decMint/60)
    #print(final)
    return(round(final,6))
    #disp=deg+chr(176)+mint+sec+'\''
    #return(disp)

def parseGPS(str):
    msg = pynmea2.parse(str)
    #print(str)
    #print ("Timestamp:",msg.timestamp)
    dispLat=calcDeg(msg.lat)
    #print("Lat:", dispLat)#,msg.lat_dir)
    dispLong=calcDeg(msg.lon)
    #print("Lon:",dispLong)#,msg.lon_dir)
    #print("\n")
    return (dispLat,dispLong)

def start():        
    port="/dev/ttyAMA0"
    serialPort = serial.Serial(port, baudrate=9600, timeout=0.5)
    flag=1

    while flag==1:
        str= serialPort.readline()
        strn=""
        for i in range(len(str)):
                #print(str[i])
            strn=strn + chr(str[i])
            #print(strn)
        if strn[0:6]=="$GPRMC":
            lat,long=parseGPS(strn)
            flag=0
    return (lat,long)
                

x=1