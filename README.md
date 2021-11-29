# Ground Station v2

Ground station software for the ACRUX-2 mission.

## Prerequisites

The easiest way to get started is with Docker.

- For most devices, see https://docs.docker.com/get-docker/
- For Raspberry Pi, see https://docs.docker.com/engine/install/debian/

## Building and running

Once you have Docker installed, running the project involves

```sh
git clone https://github.com/MelbourneSpaceProgram/ground-station-v2
cd ground-station-v2
docker compose up
```

Sometimes you will need to rebuild the image to ensure the latest changes are included

```sh
docker compose up --build
```

Stopping the project

```sh
docker compose down
```

## Modules

| Module           | Description                                       |
| ---------------- | ------------------------------------------------- |
| `ground-station` | The core of the ground station, written in Python |

## Todo

- [ ] Web dashboard
- [ ] Sat tracker
- [ ] Antenna controller (Arduino)
- [ ] Decoding and processing pipelines
  - [ ] NOAA satellites
