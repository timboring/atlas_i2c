"""Class to communicate with Atlas Scientific I2C sensors.

Source code is based on examples from Atlas Scientific:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py
"""

import io
import fcntl
import time
import copy
from typing import List, Optional, Tuple, Union

# the timeout needed to query readings and calibrations
LONG_TIMEOUT: float = 1.5
# timeout for regular commands
SHORT_TIMEOUT: float = 0.3
# the default bus for I2C on the newer Raspberry Pis, # certain older boards use bus 0
DEFAULT_BUS: int = 1
LONG_TIMEOUT_COMMANDS: Tuple[str, str] = ("R", "CAL")
SLEEP_COMMANDS: Tuple[str] = ("SLEEP",)
I2C_SLAVE = 0x703


class AtlasI2C:
    def __init__(
        self,
        address: int = None,
        name: str = None,
        bus: int = DEFAULT_BUS,
        long_timeout: float = LONG_TIMEOUT,
        short_timeout: float = SHORT_TIMEOUT,
    ) -> None:
        """Initializer."""
        self.name: Optional[str] = name
        self.bus: int = bus
        self.long_timeout = long_timeout
        self.short_timeout = short_timeout

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
        """Append the null character and sends the string over I2C."""
        cmd += "\00"
        self.device_file.write(cmd.encode("latin-1"))

    def response_valid(self, response: bytes) -> bool:
        valid: bool = True
        error_code: Optional[str] = None
        if len(response) > 0:

            error_code = str(response[0])

            # TODO: should this raise an exception instead of setting a var to False?
            if error_code != "1":  # 1:
                valid = False

        return valid

    def read(self, num_of_bytes: int = 31) -> float:
        """Read a specified number of bytes from I2C."""

        raw_data: bytes = self.device_file.read(num_of_bytes)
        is_valid: bool = self.response_valid(response=raw_data)

        if is_valid:
            data = raw_data[1:].strip().strip(b"\x00")
            result = float(data)
        else:
            pass
            # result = "Error " + self.get_device_info() + ": " + error_code

        return result

    def get_command_timeout(self, command: str) -> Optional[float]:
        timeout: Optional[float] = None
        if command.upper().startswith(LONG_TIMEOUT_COMMANDS):
            timeout = self.long_timeout
        elif not command.upper().startswith(SLEEP_COMMANDS):
            timeout = self.short_timeout

        return timeout

    def query(self, command) -> Union[float, str]:
        """Write a command to the board and read the response."""
        self.write(command)
        current_timeout: Optional[float] = self.get_command_timeout(command=command)
        if not current_timeout:
            return "sleep mode"
        else:
            time.sleep(current_timeout)
            return self.read()

    def close(self):
        self.file_read.close()
        self.file_write.close()

    def list_i2c_devices(self) -> List[int]:
        """List I2C devices.

        Valid addresses are integers between 1 - 127 per the EZO datasheets, e.g.:
        https://www.atlas-scientific.com/_files/_datasheets/_circuit/EZO_RTD_Datasheet.pdf
        """
        prev_addr: int = copy.deepcopy(self.address)
        i2c_devices: List[int] = []
        for i in range(0, 128):
            try:
                self.set_i2c_address(i)
                self.read(1)
                i2c_devices.append(i)
            except IOError:
                pass
        # restore the address we were using
        self.set_i2c_address(prev_addr)

        return i2c_devices
