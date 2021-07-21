import pyvisa


class IQTLSLaser:
    def __init__(self):
        while True:
            self.rm = pyvisa.ResourceManager()
            try:
                self.las = self.rm.open_resource("TCPIP0::192.168.95.201::inst0::INSTR")
            except:
                self.las = None
            else:
                print("Laser is ready.")

            if self.las is None:
                input("Laser not connected.\n Connect Laser and press [Enter].")
            else:
                break
        # test_las(self.las)


def set_lambda(_wl, _las):
    try:
        _las.query(f"SOUR:CHAN1:WAV {_wl}")
        # print(s)
    except:
        pass


def set_freq(_freq, _las):
    try:
        _las.query(f"SOUR:CHAN1:FREQ {_freq}")
        # print(s)
    except:
        pass


def test_las(_las):
    try:
        s = _las.query(f"*IDN?")
        print(s)
    except:
        pass


def which_wl(_las):
    try:
        s = _las.query(f"SOUR:CHAN1:WAV?")
        print(s)
    except:
        pass


if __name__ == "__main__":
    laser = IQTLSLaser()
    las = laser.las
    # start_wl = np.float(input("Set START wavelength (format 1.561419e-6): "))
    # stop_wl = np.float(input("Set  STOP wavelength (format 1.561422e-6): "))
    # step_wl = np.float(input("Set  STEP wavelength (format 0.000001e-6): "))
    # wls = np.arange(start_wl, stop_wl, step_wl)
    # for wl in wls:
    #     send_com(wl, las)
    #     secs_to_sleep = 60
    #     t1 = trange(secs_to_sleep)
    #     for ind in t1:
    #         t1.set_description(f"Current wavelength is: {wl:1.7g}")
    #         time.sleep(1)
