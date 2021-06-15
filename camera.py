import USB.NITLibrary_x64_252_py38 as NITLibrary
import logging
import time
import os
import cv2 as cv
import glob
from PIL import Image

# log level
logging.basicConfig(level=logging.INFO)


class NITCamera:
    def __init__(self):
        self.nm = NITLibrary.NITManager.getInstance()
        self.nm.forceDeviceModel(0, "NSC1401")
        self.device = None
        self.gige_cam = None
        self.agc = None
        self.snap_shot = None
        self.connect()

    def connect(self):
        self.device = self.nm.openOneDevice()
        if self.device is None:
            print("No Device Connected")
        else:
            self.gige_cam = self.device.deviceDescriptor().connectorType() == NITLibrary.ConnectorType.GIGE
            # dev.setParamValueOf("Pixel Clock", "40MHz", False)
            self.device.setParamValueOf("Exposure Time", 100.0, True)
            if self.gige_cam:
                print("GIGE CAM")
                self.device.setParamValueOf("OutputType", "RAW")
            self.agc = NITLibrary.NITToolBox.NITAutomaticGainControl()
            # myMGC = NITLibrary.GIGE.ManualGainControl(0.1, 10, dev.AgcROI("FULL_FRAME"))
            self.snap_shot = NITLibrary.NITToolBox.NITSnapshot(".\\im", "bmp")
            self.device << self.agc << self.snap_shot  # connecting s_sh to agc and dev to agc
            print("Camera is ready.")

    def shot(self, shot_name):
        self.device.start()
        time.sleep(1)
        self.snap_shot.snap()
        time.sleep(1)
        self.device.stop()

        save_as(shot_name)


def test_devs():
    nm = NITLibrary.NITManager.getInstance()
    d = nm.getDeviceDescriptor(0)
    print(f"Serial number: {d.serialNumber()}\n"
          f"{d.toString()}\n"
          f"{d.firmwareVersion()}\n"
          f"{d.connectorType()}\n"
          f"{d.connectorNumber()}\n"
          f"{d.modelId()}<--model id")


def check_screen_shot():
    file = glob.glob("*.bmp")[0]
    # path = easygui.fileopenbox(default="*.bmp", filetypes=".bmp")
    image = cv.imread(file, 0)
    cv.imshow('img', image)
    cv.waitKey(0)
    os.remove(file)


def save_as(name):
    files = glob.glob("*.bmp")
    latest_file = max(files, key=os.path.getctime)
    with Image.open(latest_file) as im:
        with open(name, 'wb') as f:
            im.save(f)
            im.close()
    os.remove(latest_file)


if __name__ == "__main__":
    cam = NITCamera()
    cam.connect()
    cam.shot("shot_01.bmp")
