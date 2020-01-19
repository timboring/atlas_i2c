from typing import List, Optional, Union

from atlas_i2c import atlas_i2c
from atlas_i2c import commands


class Sensor:
    def __init__(self, name: str, address: int = 102, commands: List = None, i2c_client=None):
        self.name = name
        self.address = address
        self.commands = commands
        self.client = i2c_client

        if not self.commands:
            self.commands = []

        if not self.client:
            self.client = atlas_i2c.AtlasI2C()

    def connect(self) -> None:
        self.client.set_i2c_address(self.address)

    def query(self, cmd: commands.Command, arguments: Optional[List[str]] = None):
        if arguments:
            command: Optional[Union[int, str]] = cmd.format_command(arguments)  # type: ignore
        else:
            command = cmd.format_command()

        response: atlas_i2c.CommandResponse = self.client.query(
            command, processing_delay=cmd.processing_delay
        )
        # TODO: this doesn't feel like the right place to set the name of this attribute
        response.sensor_name = self.name

        return response
