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
from typing import Dict, Optional

PROCESS_DELAYS_MS: Dict = {"short": 300, "long": 1500}
# TODO: think of a better way to handle this command to delay mapping
COMMAND_PROCESS_DELAYS: Dict = {
    "i": PROCESS_DELAYS_MS["short"],
    "Cal,t": PROCESS_DELAYS_MS["long"],
    "Cal,clear": PROCESS_DELAYS_MS["short"],
    "Cal,?": PROCESS_DELAYS_MS["short"],
    "R": PROCESS_DELAYS_MS["long"],
    "Status": PROCESS_DELAYS_MS["short"],
}
DEFAULT_BUS: int = 1
I2C_SLAVE = 0x0703


ERROR_CODES = {2: "SYNTAX ERROR", 254: "NOT READY", 255: "NO DATA TO SEND"}


class Error(Exception):
    pass


class ReadError(Error):
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message


class AtlasI2C:
    def __init__(self, address: int = None, name: str = None, bus: int = DEFAULT_BUS,) -> None:
        """Initializer."""
        self.name: Optional[str] = name
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

    def _check_response(self, response: bytes) -> bool:
        if len(response) > 0:
            return response[0] == 1

        return False

    def read(self, num_of_bytes: int = 31) -> float:
        """Read a specified number of bytes from I2C.

        Raises:
            ReadError when response from device is not successful (i.e. not 1)
        """

        raw_data: bytes = self.device_file.read(num_of_bytes)

        # TODO: if response is 254 (not ready), should this retry?
        if self._check_response(response=raw_data):
            data = raw_data[1:].strip().strip(b"\x00")
            result = float(data)
        else:
            raise ReadError(error_code=raw_data[0], message=ERROR_CODES[raw_data[0]])

        return result

    def query(self, command) -> float:
        """Write a command to the sensor and read the response.

        Raises:
            ReadError on any failures in self.read()
        """
        self.write(command)
        process_delay: Optional[int] = COMMAND_PROCESS_DELAYS.get(command)
        if process_delay:
            time.sleep(process_delay / 1000)

        return self.read()

    def close(self):
        self.device_file.close()
