import NITLibrary_x64_252_py38 as NITLibrary

print("""WARNING:\n
This sample program is generic for all NIT cameras.\n
The purpose is to see the main functions used to start streaming.\n
All NIT cameras have not the same set of parameters.\n
If a parameter called is not known by the camera, or if a value is passed who is not known by the camera; the SDK throw an exception catched at the end of the main function.\n
In this case you have to correct the code for your camera and recompile the application.\n
Examples:\n
-if you have an NSC1601; this one don't have a \'Gain\' parameter. The SDK will throw an exception.\n 
-if you have an NSC1601; this one don't have a \'Pixel Clock\' parameter of 40MHz. The SDK will throw an exception.\n
The purpose of the \'manual()\' is to list the parameter names known by the connected camera and the available values.\n
It is one of the first functions called in this sample\n\n
""")
input("Press enter to continue ...")

#Step 1 : Open Connected Device

#NITManager manage the connections to the cameras.
#It's the first object we deal with
#NITManager is a singleton instantiated on the first call to getInstance()

nm = NITLibrary.NITManager.getInstance() #Get unique instance of NITManager

#Open one of connected device (if it exists)

#dev = nm.openDevice(0)
dev = nm.openOneDevice()  
# If device is not open
if( dev == None ):
    print("No Device Connected")
else:
    #Step 2 : Device Configuration
    #Show manual of device
    #print(dev.manual())

    #Get param value (2 ways)
    #print("Gain:" + dev.paramStrValueOf( "Gain" )
    print("PixelDepth: " + dev.paramStrValueOf( NITLibrary.NITCatalog.PIX_DEPTH ))



    #Set param value (2 ways)
    #dev.setParamValueOf( "Pixel Clock", "40MHz", False )  #Data is not sent to the device param false
    dev.setParamValueOf("Exposure Time", 100.0, False );

    if (dev.connectorType() == NITLibrary.GIGE): #To use myAGC camera must provide a RAW data; as Gige cameras can output different data types,
    #we force RAW output type
        print("GIGE CAM")
        dev.setParamValueOf("OutputType", "RAW")

    #Fps configuration: set fps to a mean value
    min_fps = dev.minFps()
    max_fps = dev.maxFps()
    print(str(dev.minFps())+" <= " + str(dev.fps()) + " <= " + str(dev.maxFps()) )

    dev.setFps( (min_fps + max_fps)/2 , False )   #Data is not sent to the device param false
    dev.updateConfig()  #Data is sent to the device



    #Step 3 : Observers ****/
    #A NITFilter which perform Automatic Gain Control on Frames
    myAGC = NITLibrary.NITToolBox.NITAutomaticGainControl()
    #An NITCaptureObserver which display Frames with Opencv player
    myPlayer = NITLibrary.NITToolBox.NITPlayer( "My Player" )
    dev << myAGC << myPlayer
    myPlayer.connectTo(dev)
    #Start Capture!!!
        
    #First Way

    print("First Way")
    dev.start()	    #Start Capture
    input("Press Enter to stop capture...")	# Wait for User									// Wait for User
    dev.stop()      #Stop Capture

    # Second Way
    print("Second Way")
    dev.captureNFrames( 100 )	# Capture 100 Frames
    dev.waitEndCapture()	# Wait end of capture

    #Third Way
    print("Third Way")
    dev.captureForDuration( 5000 )    #Capture for 5 seconds (time in ms)
    dev.waitEndCapture()	      #Wait end of capture
    
    # Don't forget Observers Diconnection
    myAGC.disconnect()
    myPlayer.disconnect()
