# Ground Station v2

Ground station software for the ACRUX-2 mission.

## Prerequisites

The easiest way to get started is with Docker. Alternatively, you can install the packages in `requirements.txt` and run directly.

- For most devices, see https://docs.docker.com/get-docker/
- For Raspberry Pi, see https://docs.docker.com/engine/install/debian/

### EPS
The EPS script uses the following libraries and will only work when run on a Raspberry Pi.
- [Adafruit CircuitPython ADS1x15](https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15.git)
- [Raspberry GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/install/)

To reset the I2C protocol, run the following commands to disable the I2C driver
```sh
sudo rmmod i2c_dev
sudo rmmod i2c_bcm2835
```

and to re-enable it
```sh
sudo modprobe i2c_dev
sudo modprobe i2c_bcm2835
```

## Building and running

Once you have Docker installed, running the project involves

```sh
git clone https://github.com/MelbourneSpaceProgram/ground-station-v2
cd ground-station-v2
docker compose up
```

Stopping the project

```sh
docker compose down
```

## Antenna Positioning (Arduino)
The antenna's position (elevation and azimuth) is controlled by two servo motors and an arduino. The build files are TBU (to be uploaded), but the setup requires communication with the Raspberry Pi.

## Modules

| Module    | Description             |
| --------- | ----------------------- |
| `EPS`     | Checks battery voltage  |
