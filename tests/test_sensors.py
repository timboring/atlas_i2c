from unittest.mock import Mock, patch

import pytest

import commands
from sensors import Sensor
from atlas_i2c import AtlasI2C


class TestSensor:
    def test_query_without_args(self):
        i2c_client = AtlasI2C()
        i2c_client.query = Mock()
        response = commands.CommandResponse()
        response.sensor_name = "test-sensor"
        response.sensor_address = 102
        response.original_command = "R"
        response.response_type = str
        response.response_data = "1.04"
        i2c_client.query.return_value = response
        sensor = Sensor("test-sensor", i2c_client=i2c_client)
        result = sensor.query(commands.READ)
        assert isinstance(result, commands.CommandResponse)
        assert result == response

    def test_query_with_args(self):
        i2c_client = AtlasI2C()
        i2c_client.query = Mock()
        response = commands.CommandResponse()
        response.sensor_name = "test-sensor"
        response.sensor_address = 102
        response.original_command = "S,?"
        response.response_type = str
        response.response_data = "?S,c"
        i2c_client.query.return_value = response
        sensor = Sensor("test-sensor", i2c_client=i2c_client)
        result = sensor.query(commands.SCALE, arguments="?")
        assert isinstance(result, commands.CommandResponse)
        assert result == response

    def test_query_with_nonexisting_command(self):
        i2c_client = AtlasI2C()
        sensor = Sensor("test-sensor", i2c_client=i2c_client)
        with pytest.raises(AttributeError) as ex:
            sensor.query("eat")

