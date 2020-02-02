"""Class to communicate with Atlas Scientific EZO sensors in I2C mode.

Source code is based on examples from Atlas Scientific:
https://github.com/AtlasScientific/Raspberry-Pi-sample-code/blob/master/AtlasI2C.py
"""

import io
import fcntl
import time
from typing import Any, IO, Optional


DEFAULT_BUS: int = 1
I2C_SLAVE = 0x0703


class Error(Exception):
    pass


class CommandResponse:

    sensor_name: str
    sensor_address: int
    original_cmd: str
    response_type: str
    status_code: int
    data: bytes


class AtlasI2C:
    def __init__(
        self, address: int = None, bus: int = DEFAULT_BUS, device_file: IO[Any] = None,
    ) -> None:
        """Initializer."""
        self.bus: int = bus

        if not device_file:
            self.open_file()
        else:
            self.device_file: IO[Any] = device_file

        if address:
            self.set_i2c_address(address)

    def open_file(self) -> None:
        """Open /dev/i2c-BUS for reading and writing."""
        self.device_file = io.open(file=f"/dev/i2c-{self.bus}", mode="r+b", buffering=0)

    def set_i2c_address(self, addr) -> None:
        """Set I2C communication."""
        fcntl.ioctl(self.device_file, I2C_SLAVE, addr)
        self.address = addr

    def write(self, cmd: str) -> None:
        """Append the null character and send the string over I2C."""
        cmd += "\00"
        self.device_file.write(cmd.encode("latin-1"))

    def _handle_command_response(self, original_cmd: str, data: Optional[bytes]) -> CommandResponse:
        response = CommandResponse()
        response.sensor_address = self.address
        response.original_cmd = original_cmd
        if data:
            response.status_code = int(data[0])
            response.data = data[1:].strip().strip(b"\x00")
        return response

    def read(self, original_cmd: str, num_of_bytes: int = 31) -> CommandResponse:
        """Read a specified number of bytes from I2C."""
        raw_data: Optional[bytes] = self.device_file.read(num_of_bytes)

        # TODO: if response is 254 (not ready), should this retry?
        return self._handle_command_response(original_cmd, raw_data)

    def query(self, command: str, processing_delay: Optional[int] = None) -> CommandResponse:
        """Write a command to the sensor and read the response."""
        self.write(command)
        if processing_delay:
            time.sleep(processing_delay / 1000)
        return self.read(original_cmd=command)

    def close(self):
        self.device_file.close()
