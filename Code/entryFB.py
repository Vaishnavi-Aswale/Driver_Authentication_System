from firebase import firebase
from pyfingerprint.pyfingerprint import PyFingerprint
import time
import hashlib


        
def enroll(ref,firstName,lastName,licNo,lmv):
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
    f.deleteTemplate(0)
## Tries to enroll new finger
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

    ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

    ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

    ## Creates a template
        f.createTemplate()
    
    ## Saves template at new position number
        positionNumber = f.storeTemplate()
        f.loadTemplate(positionNumber, 0x01)

        scan=f.downloadCharacteristics(0x01)
        f.deleteTemplate(positionNumber)
        print('Finger scanned successfully!')

        data={
                'Name':firstName,
                'LastName':lastName,
                'LicenseNo':licNo,
                'LMV':lmv,
                'biom':scan
                }
        driverBucketId=ref.post('/DrivingLicense/details',data)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)



fbLink="https://proj-db-c86ba.firebaseio.com"
refrence=firebase.FirebaseApplication(fbLink, None)

firstName=input("Enter your First Name:")
lastName=input("Enter your Last Name:")
licNo=input("Enter yout License Number:")
lmv=int(input("Enter your status for LMV:"))

enroll(refrence,firstName,lastName,licNo,lmv)