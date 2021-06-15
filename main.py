import os
import shutil
import time
from datetime import datetime
import numpy as np
from laser import IQTLSLaser, set_freq
from camera import NITCamera
from tqdm import trange


def start_measurements(time_to_wait, f_st=400e9):
    input("Press Enter to start...")
    c = 299792458.0  # free space light speed [m/s]
    start_wl = 1530.0  # [nm]
    stop_wl = 1565.0   # [nm]
    if "y" in input("Set another range or step? [y]:"):
        print("Note. There is MAX and MIN wavelength for laser.")
        start_wl = float(input("Set START wavelength [nm] (format 1530.0): "))
        stop_wl = float(input("Set  STOP wavelength [nm] (format 1560.0): "))
        f_st = float(input("Set  STEP frequency [MHz] (format 8.5): "))
        f_st *= 1e9

    # # # transfer from wl to freq # # #
    f_stop = float(c / round(nm(round(start_wl, 1)), 12))
    f_stop = round(f_stop, 3)
    f_start = float(c / round(nm(round(stop_wl, 1)), 12))
    f_start = round(f_start, 3)

    f_s = np.arange(f_start, f_stop + f_st, f_st)

    # # # Start devices
    las = IQTLSLaser().las
    cam = NITCamera()
    # # #

    date = datetime.now().strftime("%d-%m-%Y %Hh%Mm")
    folder_name = f"S2 {date}"

    print(f"Start \u03BB: {start_wl} [nm] | Stop \u03BB {stop_wl} [nm] | Step \u03BB: {f_st:g} [Hz]")
    print(f"Data will saving at .\\{folder_name}\\shot_{{lambda}}_.bmp")

    try:
        os.mkdir(f"S2 {date}")
    except:
        pass
    t1 = trange(len(f_s))
    for i in t1:
        t1.set_description(f"Current frequency: {f_s[i]:3.7g} [Hz]")
        shot_name = f"shot_{f_s[i]:3.7g}_.bmp"

        set_freq(f_s[i], las)                               # CHANGE WAVELENGTH
        time.sleep(time_to_wait)                            # WAIT 3 seconds
        cam.shot(f"{folder_name}\\{shot_name}")  # ~ 2 sec    MAKE SHOT

    zip_name = f"{folder_name}.zip"
    shutil.make_archive(zip_name, "zip", folder_name)


def nm(wl_in_nm):
    return wl_in_nm * 1e-9


if __name__ == "__main__":
    while True:
        start_measurements(time_to_wait=0, f_st=8.5e9)
