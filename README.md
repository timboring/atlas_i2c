# AtlasI2C: A Python package to communicate with Atlas Scientific devices in I2C mode.

This package provides functionality that is based on the [example code](https://github.com/AtlasScientific/Raspberry-Pi-sample-code) from Atlas Scientific. It has the following goals:

1. Provide a simple and clean codebase with test coverage
2. Reduce code duplication by making the codebase available from PyPi
3. Provide comprehensive support for Atlas Scientific EZO sensors

# Overview
This package provides the following modules:

- [atlas_i2c](https://github.com/timboring/atlas_i2c/blob/master/src/atlas_i2c/atlas_i2c.py)
- [commands](https://github.com/timboring/atlas_i2c/blob/master/src/atlas_i2c/commands.py)
- [constants](https://github.com/timboring/atlas_i2c/blob/master/src/atlas_i2c/constants.py)
- [sensors](https://github.com/timboring/atlas_i2c/blob/master/src/atlas_i2c/sensors.py)

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
dev = atlas_i2c.Atlas_I2C()
dev.set_i2c_address(sensor_address)
dev.write("R")
time.sleep(1.5)
result = dev.read()
```

The result of calling `dev.read()` in the above code snippet is a `CommandReponse` object. Here is an example of creating a `CommandResponse` object manually and populating it:
```py
In [1]: from atlas_i2c import atlas_i2c                                                                                                 
In [2]: response = atlas_i2c.CommandResponse()                                                                                          
In [3]: response                                                                                                                        
Out[3]: <atlas_i2c.atlas_i2c.CommandResponse at 0x7fbd40f48370>
In [6]: response.sensor_address = 10                                                                                                    
In [7]: response.sensor_address = 102                                                                                                   
In [8]: response.original_cmd = "R"                                                                                                     
In [9]: response.response_type = "str"                                                                                                  
In [10]: response.status_code = raw_data[0] 
```

## module: commands
The `commands` module provides encapsulations intended to simplify interactions with sensors. Command attributes and methods can be accessed at the class level, thus it's not necessary to instantiate a command.

The module defines constants for each command class:
```py
In [19]: from atlas_i2c import commands                                                                                            
# To find the argument a command supports:
In [24]: commands.BAUD.arguments                                                                                                        
Out[24]: (300, 1200, 2400, 9600, 19200, 38400, 57600, 115200)
# To get a formatted command string:
In [25]: commands.BAUD.format_command(300)                                                                                              
Out[25]: 'Baud,300'
# A command may not support any arguments:
```
Not all commands have been implemented. The `format_command` method on unimplemented commands will raise a `NotImplementedError` exception.

## module: sensors
The `sensors` module provides a higher-level encapsulation of a sensor in the form of the `Sensor` class. The intention is that the `Sensor` class is used as the primary means of communication; it uses the lower-level `AtlasI2C` class to perform all functions, such as reading data from a sensor.

```py
In [31]: from atlas_i2c import sensors                                                                                                  
In [32]: sensor = sensors.Sensor("Temperature", 102)                                                                                    
In [33]: sensor.connect() 
In [34]: response = sensor.query(commands.READ)
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
> pip install atlas-i2c
```

## From source
```sh
> python setup.py bdist_wheel
> pip install dist/atlas_i2c-$version-py3-none-any.whl
```

# Atlas Scientific Sensor Datasheets
- [pH](https://www.atlas-scientific.com/_files/_datasheets/_circuit/pH_EZO_Datasheet.pdf)
- [temp](https://www.atlas-scientific.com/_files/_datasheets/_circuit/EZO_RTD_Datasheet.pdf)
- [orp](https://www.atlas-scientific.com/_files/_datasheets/_circuit/ORP_EZO_datasheet.pdf)
- [do](https://www.atlas-scientific.com/_files/_datasheets/_circuit/DO_EZO_Datasheet.pdf)
- [ec](https://www.atlas-scientific.com/_files/_datasheets/_circuit/EC_EZO_Datasheet.pdf)
- [co2](https://www.atlas-scientific.com/_files/_datasheets/_probe/EZO_CO2_Datasheet.pdf)
- [flo](https://www.atlas-scientific.com/_files/_datasheets/_circuit/flow_EZO_Datasheet.pdf)
