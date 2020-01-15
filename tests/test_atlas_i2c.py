import io
import tempfile
from tarfile import ReadError
from unittest.mock import Mock

import pytest

from atlas_i2c import AtlasI2C, ReadError
import commands
import constants

GOOD_RESPONSE = b"\x011.642\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
ERROR_RESPONSE = b"\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
NO_DATA_RESPONSE = b"\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
NOT_READY_RESPONSE = b"\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


class TestAtlasI2C:
    @pytest.mark.parametrize(
        "command",
        [
            "Baud,9600",
            "Cal,?",
            "D,?",
            "Export,?",
            "Factory",
            "Find",
            "i",
            "I2C,100",
            "L,?",
            "M,?",
            "Plock,?",
            "R",
            "S,?",
            "Sleep",
            "Status",
        ],
    )
    def test_write(self, command):
        device_file = io.BytesIO()
        dev = AtlasI2C()
        dev.address = 102
        dev.device_file = device_file
        dev.write(command)

    def test_read(self):
        device_file = io.BytesIO(GOOD_RESPONSE)
        dev = AtlasI2C()
        dev.address = 102
        dev.device_file = device_file
        response = dev.read(original_cmd="R")
        assert isinstance(response, commands.CommandResponse)
