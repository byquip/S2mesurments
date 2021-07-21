import logging
import os
import numpy as np
from camera import NITCamera

# log level
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    cam = NITCamera()
    cam.connect()

    li = np.arange(0, 8, 0.25)
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

        cam.device.setParamValueOf("Gain", str(gain))
        cam.device.setParamValueOf("Offset", "50.0")
        gain_get = cam.device.paramStrValueOf("Gain")
        offset_get = cam.device.paramStrValueOf("Offset")
        print(f"recognized gain:{gain_get}\nproposed gain: {gain}\noffset: {offset_get}\n")
        shot_name = f"gain_{gain_get}.bmp"
        cam.shot(f"{folder_name}\\{shot_name}")
        # check_screen_shot()
    print(f"check folder:\"{folder_name}\" for screens")
