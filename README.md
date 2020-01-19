# AtlasI2C: A Python package to communicate with Atlas Scientific devices in I2C mode.

This package provides functionality that is based on the [example code](https://github.com/AtlasScientific/Raspberry-Pi-sample-code) from Atlas Scientific. It has the following goals:

1. Provide a simple and clean codebase with test coverage
2. Reduce code duplication by making the codebase available from PyPi
3. Provide comprehensive support for Atlas Scientific EZO sensors

# Overview
This package provides the following modules:

- [atlas_i2c](src/atlas_i2c.py)
- [commands](src/commands.py)
- [constants](src/constants.py)
- [sensors](src/sensors.py)

## module: atlas_i2c
The `atlas_i2c` module can be thought of as the client that talks to the server, similar to how an HTTP client talks to an HTTP server. The server in this scenario is the Atlas Scientfic EZO sensor. Instead of talking over TCP using HTTP, however, it talks to the server over the I2C bus, using Linux device files (e.g. `/dev/-i2c-1`).

The module uses the following protocol to communicate with a sensor:
1. Open the device file for reading and writing
2. Send a command string (e.g. "R") to the device by writing it to the device file
3. Wait for N milliseconds for the sensor to process the command
4. Read the resulting data from the device file

Using this module to communicate with a sensor looks like the following:
```py
import fcntl
import time

from atlas_i2c import atlas_i2c

sensor_address = 102
fd = open("/dev/i2c-1", "r+b")
fcnt.iotl(fd, 0x703, sensor_address)
dev = atlas_i2c.Atlas_I2C()
dev.set_i2c_address(sensor_address)
dev.write("R")
time.sleep(1.5)
result = dev.read()
```

# Supported Python Versions
This module requires Python >= 3.6.

# Tests
`atlas_i2c` uses Tox for test automation, which includes linting, formatting and static type checking. To run Tox:

```sh
> tox
[output truncated]
py38: commands succeeded
py37: commands succeeded
py36: commands succeeded
mypy: commands succeeded
lint: commands succeeded
format: commands succeeded
congratulations :)
```

# Installation
## From PyPi
Installation can be done using Pip:

```sh
> pip install atlas_i2c
```

## From source
```sh
> python setup.py bdist_wheel
> pip install dist/atlas_i2c-$version-py3-none-any.whl
```

# Usage
```py
from atlas_i2c import AtlasI2C

dev = AtlasI2C()
dev.set_i2c_address(102)
print(dev.query("R"))  # returns a reading from the I2C sensor as a float
```
