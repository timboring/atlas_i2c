# AtlasI2C: Class to communicate with Atlas Scientific devices in I2C mode.

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
