import os
import shutil
import time
from datetime import datetime
import numpy as np
from laser import IQTLSLaser, set_freq
from camera import NITCamera
from tqdm import trange
import parameters


def start_measurements(time_to_wait, f_st=8.5):
    input("Press Enter to start...")
    c = 299792458.0  # free space light speed [m/s]
    start_wl = 1530.0  # [nm]
    stop_wl = 1565.0   # [nm]
    print(f"start with \u03BB range: {start_wl}-{stop_wl} [nm] and frequency step: {f_st} [GHz]")
    if "y" in input("set another range or step? [y]:"):
        print("Note. There is MAX and MIN wavelength for laser.")
        start_wl = float(input("Set START wavelength [nm] (format 1530.0): "))
        stop_wl = float(input("Set  STOP wavelength [nm] (format 1560.0): "))
        f_st = float(input("Set  STEP frequency [GHz] (format 8.5): "))
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

    date = datetime.now().strftime("%d-%m-%Y %Hh%Mm")
    folder_name = f"S2 {date}"

    print(f"Start \u03BB: {start_wl} [nm] | Stop \u03BB {stop_wl} [nm] | Step \u03BB: {f_st:g} [Hz]")
    print(f"Data will saving at .\\{folder_name}\\shot_{{lambda}}_.bmp  lambda in [nm]")

    try:
        os.mkdir(folder_name)
    except:
        pass

    t1 = trange(len(f_s))
    for i in t1:
        t1.set_description(f"Current frequency: {f_s[i]:3.7g} [Hz]")
        # freq -> wl
        current_wavelength = float(c / f_s[i]) * 1e9
        current_wavelength = round(current_wavelength, 5)
        shot_name = f"shot_{current_wavelength:.5f}_.bmp"

        set_freq(f_s[i], las)                               # CHANGE WAVELENGTH
        time.sleep(time_to_wait)                            # WAIT 3 seconds
        cam.shot(f"{folder_name}\\{shot_name}")  # ~ 2 sec    MAKE SHOT

    zip_name = f"{folder_name}.zip"
    shutil.make_archive(zip_name, "zip", folder_name)
    print(f"check folder:\"{folder_name}\" for screens")


def nm(wl_in_nm):
    return wl_in_nm * 1e-9


if __name__ == "__main__":
    while True:
        start_measurements(time_to_wait=parameters.shot_delay, f_st=8.5)
