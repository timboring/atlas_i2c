import io
from unittest.mock import Mock, patch

import pytest

from atlas_i2c import commands
from atlas_i2c import sensors
from atlas_i2c import atlas_i2c


class TestSensor:
    def test_query_without_args(self, good_response):
        device_file = io.BytesIO()
        i2c_client = atlas_i2c.AtlasI2C(device_file=device_file)
        i2c_client.query = Mock()
        response = atlas_i2c.CommandResponse()
        response.sensor_name = "test-sensor"
        response.sensor_address = 102
        response.original_command = "R"
        response.response_type = str
        response.response_data = good_response
        i2c_client.query.return_value = response
        sensor = sensors.Sensor("test-sensor", i2c_client=i2c_client)
        result = sensor.query(commands.READ)
        assert isinstance(result, atlas_i2c.CommandResponse)
        assert result == response

    def test_query_with_args(self):
        device_file = io.BytesIO()
        i2c_client = atlas_i2c.AtlasI2C(device_file=device_file)
        i2c_client.query = Mock()
        response = atlas_i2c.CommandResponse()
        response.sensor_name = "test-sensor"
        response.sensor_address = 102
        response.original_command = "S,?"
        response.response_type = str
        response.response_data = "?S,c"
        i2c_client.query.return_value = response
        sensor = sensors.Sensor("test-sensor", i2c_client=i2c_client)
        result = sensor.query(commands.SCALE, arguments="?")
        assert isinstance(result, atlas_i2c.CommandResponse)
        assert result == response

    def test_query_with_nonexisting_command(self):
        device_file = io.BytesIO()
        i2c_client = atlas_i2c.AtlasI2C(device_file=device_file)
        sensor = sensors.Sensor("test-sensor", i2c_client=i2c_client)
        with pytest.raises(AttributeError) as ex:
            sensor.query("eat")

