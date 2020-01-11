import io
import tempfile
from tarfile import ReadError
from unittest.mock import Mock

import pytest
from AtlasI2C import AtlasI2C, ReadError, ERROR_CODES

GOOD_RESPONSE = b"\x011.642\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
ERROR_RESPONSE = b"\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
NO_DATA_RESPONSE = b"\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
NOT_READY_RESPONSE = b"\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


class TestAtlasI2C:
    def test_init(self):
        dev = AtlasI2C()
        assert isinstance(dev, AtlasI2C)

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
        dev.device_file = device_file
        dev.write(command)

    def test_check_good_response(self):
        dev = AtlasI2C()
        assert dev._check_response(GOOD_RESPONSE)

    @pytest.mark.parametrize("response", [ERROR_RESPONSE, NO_DATA_RESPONSE, NOT_READY_RESPONSE,])
    def test_check_not_ready_response(self, response):
        dev = AtlasI2C()
        assert not dev._check_response(response)

    def test_read(self):
        device_file = io.BytesIO(GOOD_RESPONSE)
        dev = AtlasI2C()
        dev.device_file = device_file
        response = dev.read()
        assert isinstance(response, float)

    @pytest.mark.parametrize("response", [ERROR_RESPONSE, NO_DATA_RESPONSE, NOT_READY_RESPONSE])
    def test_read_with_error_response(self, response):
        device_file = io.BytesIO(response)
        dev = AtlasI2C()
        dev.device_file = device_file
        with pytest.raises(ReadError) as ex:
            response = dev.read()
        assert ex.value.error_code == response[0]
        assert ex.value.message == ERROR_CODES[response[0]]
