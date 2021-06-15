import NITLibrary_x64_252_py38 as NITLibrary
import numpy
import time

#Creation of our custom filters and observers

class myPyFilter(NITLibrary.NITUserFilter):
    def __init__(self, fifoSize = 10):      
        NITLibrary.NITUserFilter.__init__(self, fifoSize)
    def onStart(self):      #You may not define this function - It will be called when the camera start the acquisition
        print("start filter")
    def onNewFrame(self, array, info):   #You MUST define this function - It will be called on each frames
        new_array = numpy.invert(array)
        return new_array        #Don't forget to return the resulting array
    def onStop(self):       #You may not define this function - It will be called when the camera stop the acquisition
        print("stop filter")

class myPyObserver(NITLibrary.NITUserObserver):
    def onStart(self):      #You may not define this function
        "Your code goes here"
    def onNewFrame(self, array, info):  #You MUST define this function
        "Your code goes here"
    def onStop(self):      #You may not define this function
        "Your code goes here"  

#Step 1 : Open Connected Device

#NITManager manage the connections to the cameras.
#It's the first object we deal with
#NITManager is a singleton instantiated on the first call to getInstance()

nm = NITLibrary.NITManager.getInstance() #Get unique instance of NITManager

deviceCount = nm.deviceCount()


# nm.forceDeviceModel(0, "NSC0803") #force device if you camera info line has not be detected
# dev = nm.openDevice(0)
dev = nm.openOneDevice()

#**************************************************

#If device is not open

if dev == None:
    print("No device connected")
else:
    gige_cam = dev.deviceDescriptor().connectorType() == NITLibrary.ConnectorType.GIGE #get the type of camera

    #The following code is a general way to iterate throught parameters for USB and GIGE cameras. For USB cameras only it could be much simpler :
    """
    for param in dev:
        print(param.name())
        for value in param:
            print(value)
    """
    #This work for any camera
    for param in dev:
        print("-------------------------")
        print("Name :        "+str(param.name()))
        print("Is Inert :    "+str(param.isInert()))
        val_type = param.valueType()
        if(gige_cam and param.isContinuous()): #This can be true only for GIGE cameras
            print("From : "+str(param.minValue())+" to "+str(param.maxValue()))
            if val_type != "Float":
                print("By step of"+str(param.step()))
        else:
            if gige_cam and val_type=="String": #This can be true only for GIGE cameras
                print("String parameter")
            # else: #This is true for any type of camera
            #     if val_type:
            #         print("type : " +val_type)
            #     i = 1
            #     for value in param:
            #         print(value, end=' ')
            #         if i%5==0:
            #             print("\n")
            #         i = i+1
        print("\n----------------------\n")
                
    #To do the next step we set the camera to output raw data if it's a Gige camera
    if (gige_cam): 
        #we force RAW output type
        print("GIGE CAM")
        dev.setParamValueOf("OutputType", "RAW")
 

    mpf = myPyFilter()

    mpo = myPyObserver()

    myAGC = NITLibrary.NITToolBox.NITAutomaticGainControl()

    myAGCPlayer = NITLibrary.NITToolBox.NITPlayer( "(AGC) Player" )
    myFilterPlayer = NITLibrary.NITToolBox.NITPlayer( "(AGC + MyFilter) Player")

    dev << myAGC << myAGCPlayer
    myAGC << mpf << myFilterPlayer

    #Which is equivalent to
    """
    myAGC.connectTo( dev )
    myAGCPlayer.connectTo( myAGC )

    mpf.connectTo( myAGC )
    myFilterPlayer.connectTo( mpf )
    """
    #Start capture
    input("Start capture")
    print("Capture")
    """
    dev.captureForDuration(5000)
    dev.waitEndCapture()
    """
    dev.start()     #Start capture
    input("Press a key to end capture")
    dev.stop()      #Stop capture"""
    



