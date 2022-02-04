#!/usr/bin/env python3

from ground_station import GroundStation

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

if __name__ == "__main__":
    print("Launching ground station")
    station = GroundStation(is_raspberrypi())
    station.start()
