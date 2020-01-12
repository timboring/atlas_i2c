# AtlasI2C: A Python module to communicate with Atlas Scientific devices in I2C mode.

This module is based on the [example code](https://github.com/AtlasScientific/Raspberry-Pi-sample-code) from Atlas Scientific. It has the following goals:

1. Provide a simple and clean codebase with test coverage
2. Reduce code duplication by making the codebase available from PyPi
3. Provide comprehensive support for Atlas Scientific EZO sensors

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
