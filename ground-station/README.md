# Ground station

The core logic for the ground station.

## Building and running

You can build and run the ground station directly using

```sh
docker build -t ground-station .
docker run \
  --name ground-station \
  --mount type=bind,src="$(pwd)"/.,dst=/usr/app \
  --mount type=volume,dst=/app/data \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e PYTHONUNBUFFERED=1 \
  ground-station
```

## Testing

To run the test cases, you will need `pytest` installed. Then, calling `pytest .` in the root directory will automatically find and run all tests.
