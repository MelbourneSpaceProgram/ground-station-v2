# Ground Station v2

Ground station software for the ACRUX-2 mission.

## Prerequisites

The easiest way to get started is with Docker.

- For most devices, see https://docs.docker.com/get-docker/
- For Raspberry Pi, see https://docs.docker.com/engine/install/debian/

Tests are written using `pytest` which can be installed to your default environment using

```sh
pip install --user pytest
```

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

## Testing

Calling `pytest` in the root directory will automatically find and run all tests.

```sh
pytest .
```

## Modules

| Module    | Description             |
| --------- | ----------------------- |
| `tracker` | Tracks satellite passes |

## Todo

- [ ] Sat tracker
- [ ] Antenna controller (Arduino)
- [ ] Decoding and processing pipelines
  - [ ] NOAA satellites
- [ ] Web dashboard
  - [ ] Move into separate repository?
