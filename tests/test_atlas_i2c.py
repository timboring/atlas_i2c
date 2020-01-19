import io
import tempfile
from tarfile import ReadError
from unittest.mock import Mock

import pytest

from atlas_i2c import atlas_i2c
from atlas_i2c import commands
from atlas_i2c import constants


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
        dev = atlas_i2c.AtlasI2C()
        dev.address = 102
        dev.device_file = device_file
        dev.write(command)

    def test_read(self, good_response, error_response, no_data_response, not_ready_response):
        for response in (good_response, error_response, no_data_response, not_ready_response):
            device_file = io.BytesIO(response)
            dev = atlas_i2c.AtlasI2C()
            dev.address = 102
            dev.device_file = device_file
            response = dev.read(original_cmd="R")
            assert isinstance(response, atlas_i2c.CommandResponse)
