from abc import ABC, abstractclassmethod
from typing import Any, Optional, Tuple, Union


class Error(Exception):
    pass


class ArgumentError(Error):
    pass


class CommandDoesNotExistError(Error):
    pass


class CommandClassDoesNotExistError(Error):
    pass


class CommandResponse:

    sensor_name: str
    sensor_address: int
    original_cmd: str
    response_type: str
    status_code: int
    data: bytes


class Command(ABC):
    arguments: Any
    name: str
    processing_delay: Optional[int]

    @abstractclassmethod
    def format_command(cls):
        raise NotImplementedError


class Baud(Command):

    arguments: Tuple[int, int, int, int, int, int, int, int] = (
        300,
        1200,
        2400,
        9600,
        19200,
        38400,
        57600,
        115200,
    )
    name: str = "Baud"
    processing_delay: None = None

    @classmethod
    def format_command(cls, arg: int = 9600) -> str:
        """Format command string.

        Defaults to 9600, which will reboot the sensor in UART mode.
        """
        if arg not in cls.arguments:
            raise ArgumentError(f"arg not one of {cls.arguments}")
        return f"{cls.name},{arg}"


class Calibrate(Command):
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Export(Command):
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Factory(Command):

    arguments: None = None
    name: str = "Factory"
    processing_delay: None = None

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Find(Command):
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Info(Command):

    arguments: None = None
    name: str = "i"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class I2C(Command):

    addresses = tuple(range(1, 128))
    name: str = "I2C"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, address: int = 102) -> str:
        """Format command string.

        Defaults to 102, which is the default address for the EZO RTD temp sensor.
        """
        if address not in cls.addresses:
            raise ArgumentError(f"address {address} not in range 1-127")
        return f"{cls.name},{address}"


class Import(Command):
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Led(Command):
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class PLock(Command):

    arguments: Tuple[int, int, str] = (1, 0, "?")
    name: str = "Plock"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: Union[int, str] = "?") -> str:
        if arg not in cls.arguments:
            raise ArgumentError(f"{arg} not one of {cls.arguments}")
        return f"{cls.name},{arg}"


class Read(Command):

    arguments: None = None
    name: str = "R"
    processing_delay: int = 1500

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Salinity(Command):

    arguments: None = None
    name: str = "S"
    processing_delay: int = 300

    @classmethod
    def format_command(
        cls,
        value: Optional[int] = None,
        ppt: Optional[bool] = None,
        question: Optional[bool] = None,
    ) -> Optional[str]:
        if all((value, ppt, question)):
            raise ArgumentError(f"You cannot specify all of [question, value, ppt]")

        if not any((question, value)):
            raise ArgumentError(f"You must specify at least one of [value=n | question]")

        if value:
            formatted_cmd: str = f"{cls.name},{value}"

        if ppt:
            formatted_cmd += ",ppt"

        if question:
            formatted_cmd = f"{cls.name},?"

        return formatted_cmd


class Scale(Command):

    arguments: Tuple[str, str, str, str] = ("c", "k", "f", "?")
    name: str = "S"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: str = "c") -> str:
        if arg not in cls.arguments:
            raise ArgumentError(f"{arg} is not one of {cls.arguments}")

        return f"{cls.name},{arg}"


class Sleep(Command):

    arguments: None = None
    name: str = "Sleep"
    processing_delay: None = None

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Status(Command):

    arguments: None = None
    name: str = "Status"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


BAUD = Baud
CALIBRATE = Calibrate
EXPORT = Export
FACTORY = Factory
FIND = Find
I2C = I2C
INFO = Info
IMPORT = Import
LED = Led
PLOCK = PLock
READ = Read
SALINITY = Salinity
SCALE = Scale
SLEEP = Sleep
STATUS = Status
