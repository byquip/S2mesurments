import NITLibrary_x64_252_py38 as NITLibrary

#NITManager manage the connections to the cameras.
#It's the first object we deal with
#NITManager is a singleton instantiated on the first call to getInstance()

ui = NITLibrary.NITToolBox.NITCommandLineUI()

dev = ui.chooseDevice()

if (dev.connectorType() == NITLibrary.GIGE):
        print("GIGE CAM")
        dev.setParamValueOf("OutputType", "RAW")

if dev != None:
    #Make Connections
    myAGC = NITLibrary.NITToolBox.NITAutomaticGainControl()
    agcPlayer = NITLibrary.NITToolBox.NITPlayer("Player with AGC")

    dev << myAGC << agcPlayer

    ui.controlDevice(dev)
else:
    print("Device Diconected")
