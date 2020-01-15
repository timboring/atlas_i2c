"""Class to communicate with Atlas Scientific EZO sensors in I2C mode.

Source code is based on examples from Atlas Scientific:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py

Relevant datasheets for each of the EZO sensors:
pH: https://www.atlas-scientific.com/_files/_datasheets/_circuit/pH_EZO_Datasheet.pdf
temp: https://www.atlas-scientific.com/_files/_datasheets/_circuit/EZO_RTD_Datasheet.pdf
orp: https://www.atlas-scientific.com/_files/_datasheets/_circuit/ORP_EZO_datasheet.pdf
do: https://www.atlas-scientific.com/_files/_datasheets/_circuit/DO_EZO_Datasheet.pdf
ec: https://www.atlas-scientific.com/_files/_datasheets/_circuit/EC_EZO_Datasheet.pdf
co2: https://www.atlas-scientific.com/_files/_datasheets/_probe/EZO_CO2_Datasheet.pdf
flo: https://www.atlas-scientific.com/_files/_datasheets/_circuit/flow_EZO_Datasheet.pdf
"""

import io
import fcntl
import time

import commands

DEFAULT_BUS: int = 1
I2C_SLAVE = 0x0703


class Error(Exception):
    pass


class ReadError(Error):
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message


class AtlasI2C:
    def __init__(self, address: int = None, bus: int = DEFAULT_BUS,) -> None:
        """Initializer."""
        self.bus: int = bus

        if address:
            self.set_i2c_address(address)

    def open_file(self, device_file: str = "/dev/i2c-{}") -> None:
        self.device_file = io.open(file=device_file.format(self.bus), mode="r+b", buffering=0)

    def set_i2c_address(self, addr) -> None:
        """Set I2C communication."""
        self.open_file()
        fcntl.ioctl(self.device_file, I2C_SLAVE, addr)
        self.address = addr

    def write(self, cmd: str) -> None:
        """Append the null character and send the string over I2C."""
        cmd += "\00"
        self.device_file.write(cmd.encode("latin-1"))

    def _handle_command_response(self, original_cmd: str, data: bytes) -> commands.CommandResponse:
        response = commands.CommandResponse()
        response.sensor_address = self.address
        response.original_cmd = original_cmd
        response.status_code = int(data[0])
        response.data = str(data[1:].strip().strip(b"\x00"))
        return response

    def read(self, original_cmd: str, num_of_bytes: int = 31) -> commands.CommandResponse:
        """Read a specified number of bytes from I2C.

        Raises:
            ReadError when response from device is not successful (i.e. not 1)
        """

        raw_data: bytes = self.device_file.read(num_of_bytes)

        # TODO: if response is 254 (not ready), should this retry?
        result: commands.CommandResponse = self._handle_command_response(original_cmd, raw_data)
        return result

    def query(self, command: str, processing_delay: int = 300) -> commands.CommandResponse:
        """Write a command to the sensor and read the response.

        Raises:
            ReadError on any failures in self.read()
        """
        self.write(command)
        time.sleep(processing_delay / 1000)
        return self.read(original_cmd=command)

    def close(self):
        self.device_file.close()
