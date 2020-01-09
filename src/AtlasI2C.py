"""Class to communicate with Atlas Scientific I2C sensors.

Source code taken from Atlas Scientific examples:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py
"""

import io
import fcntl
import time
import copy
from typing import List, Optional, Tuple

# the timeout needed to query readings and calibrations
LONG_TIMEOUT: float = 1.5
# timeout for regular commands
SHORT_TIMEOUT: float = 0.3
# the default bus for I2C on the newer Raspberry Pis, # certain older boards use bus 0
DEFAULT_BUS: int = 1
# the default address for the sensor
DEFAULT_ADDRESS: int = 98
LONG_TIMEOUT_COMMANDS: Tuple[str, str] = ("R", "CAL")
SLEEP_COMMANDS: Tuple[str] = ("SLEEP",)


class AtlasI2C:
    def __init__(
        self,
        address: int = DEFAULT_ADDRESS,
        name: str = None,
        bus: int = DEFAULT_BUS,
        long_timeout: float = LONG_TIMEOUT,
        short_timeout: float = SHORT_TIMEOUT,
    ) -> None:
        """Initializer."""
        self.address: int = address
        self.name: Optional[str] = name
        self.bus: int = bus
        self.long_timeout = long_timeout
        self.short_timeout = short_timeout

    def open_file_streams(
        self, read_file: str = "/dev/i2c-{}", write_file: str = "/dev/i2c-{}"
    ) -> None:
        # TODO: do we actually need two streams?
        self.file_read = io.open(file=read_file.format(self.bus), mode="rb", buffering=0)
        self.file_write = io.open(file=write_file.format(self.bus), mode="wb", buffering=0)

    def set_i2c_address(self, addr) -> None:
        """Set I2C communication."""
        # TODO: what is this actually doing? and should I2C_SLAVE be hardcoded like this?
        I2C_SLAVE = 0x703
        fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
        self.address = addr

    def write(self, cmd: str) -> None:
        """Append the null character and sends the string over I2C."""
        cmd += "\00"
        self.file_write.write(cmd.encode("latin-1"))

    def _handle_raspi_glitch(self, response) -> List[str]:
        """
        Change MSB to 0 for all received characters except the first
        and get a list of characters
        NOTE: having to change the MSB to 0 is a glitch in the raspberry pi,
        and you shouldn't have to do this!

        TODO(tboring): figure out what this is really doing and what the "glitch" is
        """
        return list(map(lambda x: chr(x & ~0x80), list(response)))

    def response_valid(self, response: bytes) -> Tuple[bool, Optional[str]]:
        valid: bool = True
        error_code: Optional[str] = None
        if len(response) > 0:

            error_code = str(response[0])

            # TODO: should this raise an exception instead of setting a var to False?
            if error_code != "1":  # 1:
                valid = False

        return valid, error_code

    def get_device_info(self):
        if self._name == "":
            return self._module + " " + str(self.address)
        else:
            return self._module + " " + str(self.address) + " " + self._name

    def read(self, num_of_bytes: int = 31) -> str:
        """Read a specified number of bytes from I2C."""

        raw_data: bytes = self.file_read.read(num_of_bytes)
        # TODO: how to specify types when when unpacking a tuple
        is_valid, error_code = self.response_valid(response=raw_data)

        if is_valid:
            char_list: List[str] = self._handle_raspi_glitch(raw_data[1:])
            # TODO: why build a string instead of just returning the actual data as a float?
            result = "Success " + self.get_device_info() + ": " + str("".join(char_list))
        else:
            result = "Error " + self.get_device_info() + ": " + error_code

        return result

    def get_command_timeout(self, command: str) -> Optional[float]:
        timeout: Optional[float] = None
        if command.upper().startswith(LONG_TIMEOUT_COMMANDS):
            timeout = self.long_timeout
        elif not command.upper().startswith(SLEEP_COMMANDS):
            timeout = self.short_timeout

        return timeout

    def query(self, command) -> str:
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

    def list_i2c_devices(self) -> List:
        prev_addr: int = copy.deepcopy(self.address)
        i2c_devices: List = []
        # TODO: since this is targeted to Atlas Scientific devices, do we need to check from 0-128?
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
