import logging
import os
import numpy as np
from camera import NITCamera

# log level
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    cam = NITCamera()
    cam.connect()

    li = np.arange(0, 2.5, 0.25)
    li = np.append(li, 4.0)
    print(li)
    # date = datetime.now().strftime("%d-%m-%Y %Hh%Mm")
    folder_name = f"S2 offset test"
    try:
        os.remove(folder_name)
    except:
        pass
    try:
        os.mkdir(folder_name)
    except:
        pass
    li = np.arange(50, 61, 1)
    gain = str(input("Set Gain [0(AGC), 0.25, 0.5 0.75 1.0 1.25 1.5 1.75 2.0 2.25 4.0]: "))
    cam.device.setParamValueOf("Gain", gain)
    for ofs in li:
        s = int(ofs)
        shot_name = f"ofs_{s}.bmp"
        cam.device.setParamValueOf("Offset", str(ofs))
        gain_get = cam.device.paramStrValueOf("Gain")
        offset_get = cam.device.paramStrValueOf("Offset")
        print(offset_get, ofs)
        print(f"recognized offset:{offset_get}\nproposed offset: {ofs}\ngain: {gain_get}\n")
        cam.shot(f"{folder_name}\\{shot_name}")
    print(f"check folder:\"{folder_name}\" for screens")
