from datetime import datetime

import USB.NITLibrary_x64_252_py38 as NITLibrary
import logging
import time
import os
import cv2 as cv
import glob
from PIL import Image
import numpy as np
import parameters

# log level
logging.basicConfig(level=logging.INFO)


class NITCamera:
    def __init__(self):
        self.nm = NITLibrary.NITManager.getInstance()
        # self.nm.forceDeviceModel(0, "NSC1401")  # (NSC0803|NSC0902|NSC1104|NSC1201|NSC1231|NSC1401|NSC1602)
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
            print(self.device.manual())
            if self.gige_cam:
                print("GIGE CAM")

                self.device.setParamValueOf("OutputType", "RAW")
            self.agc = NITLibrary.NITToolBox.NITAutomaticGainControl()
            # agcroi = NITLibrary.AgcROI("FULL_FRAME")
            # agcroicustom = NITLibrary.AgcROICustom(0, 0, 320, 256)
            # print(f"{agcroi=}\n{agcroicustom=}")
            # self.myMGC = NITLibrary.GIGE.ManualGainControl(0.0, 1.0, agcroi)  #  NITLibrary.AgcROI("FULL_FRAME")
            # self.nuc = NITLibrary.GIGE.NUC1Point()
            # print(f"{dir(NITLibrary.GIGE.ManualGainControl)=}")
            # print(f"{dir(NITLibrary)=}")
            # print(f"{dir(self.myMGC)=}")
            # print(f"{dir(self.nuc)=}")
            # print(f"{dir(self.agc)=}")
            # s = NITLibrary.NITToolBox.ManualGainControl(0.1, 10.0, NITLibrary.AgcROICustom(0, 0, 320, 256))
            # print(f"{s=}")
            self.snap_shot = NITLibrary.NITToolBox.NITSnapshot(".\\im", "bmp")
            # print("2")
            # self.device << myMGC << self.snap_shot  # connecting s_sh to agc and dev to agc
            # self.device << self.myMGC << self.snap_shot
            # self.myMGC.connectTo(self.device)
            # print("3")
            # self.snap_shot.connectTo(self.myMGC)
            # self.snap_shot.connectTo(self.device)
            self.device.setParamValueOf("Gain", parameters.cam_gain)
            self.device.setParamValueOf("Offset", parameters.cam_offset)
            self.device <<self.snap_shot  # connecting s_sh to agc and dev to agc

            print("Camera is ready.")

            # dev << myAGC << myAGCPlayer
            # myAGC.connectTo(dev)
            # myAGCPlayer.connectTo(myAGC)

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
    if len(files) < 1:
        print("PICTURE DONT SAVED")
        return
    latest_file = max(files, key=os.path.getctime)
    with Image.open(latest_file) as im:
        with open(name, 'wb') as f:
            im.save(f)
            im.close()
    os.remove(latest_file)


if __name__ == "__main__":
    cam = NITCamera()
    cam.connect()

    li = np.arange(0, 2.5, 0.25)
    li = np.append(li, 4.0)
    print(li)
    # date = datetime.now().strftime("%d-%m-%Y %Hh%Mm")
    folder_name = f"S2 gain test"
    try:
        os.remove(folder_name)
    except:
        pass
    try:
        os.mkdir(folder_name)
    except:
        pass
    for gain in li:
        s = int(gain*100)
        shot_name = f"gain_{s}.bmp"
        cam.device.setParamValueOf("Gain", str(gain))
        cam.device.setParamValueOf("Offset", "50.0")
        gain_get = cam.device.paramStrValueOf("Gain")
        offset_get = cam.device.paramStrValueOf("Offset")
        print(gain_get, gain, offset_get)
        cam.shot(f"{folder_name}\\{shot_name}")
        # check_screen_shot()
    li = np.arange(50, 61, 1)
    cam.device.setParamValueOf("Gain", "0.25")
    for ofs in li:
        s = int(ofs)
        shot_name = f"ofs_{s}.bmp"
        # cam.device.setParamValueOf("Gain", str(gain))
        cam.device.setParamValueOf("Offset", str(ofs))
        # gain_get = cam.device.paramStrValueOf("Gain")
        offset_get = cam.device.paramStrValueOf("Offset")
        print(offset_get, ofs)
        cam.shot(f"{folder_name}\\{shot_name}")
