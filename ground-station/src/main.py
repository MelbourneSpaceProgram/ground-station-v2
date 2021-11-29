#!/usr/bin/env python3

from ground_station import GroundStation

if __name__ == "__main__":
    print("Launching ground station")
    station = GroundStation()
    station.start()
