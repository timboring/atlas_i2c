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
    """Set device baud rate; used to switch from I2C to UART mode."""

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
    # NB: This command is complicated, because sensors have different calibration arguments
    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class DataLogger(Command):
    """Enable/disable data logger."""

    arguments: Tuple[Tuple, str] = (tuple(range(0, 32001)), "?")
    name: str = "DataLogger"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: Union[int, str] = "?") -> str:
        if arg not in cls.arguments and arg not in cls.arguments[0]:
            raise ArgumentError(f"{arg} must be in range(0, 32001) or '?'")
        return f"{cls.name},{arg}"


class Export(Command):
    """Export calibration settings."""

    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Factory(Command):
    """Factory reset."""

    arguments: None = None
    name: str = "Factory"
    processing_delay: None = None

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Find(Command):
    """Find a device by making the LED rapidly blink white."""

    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Info(Command):
    """Get info about a device."""

    arguments: None = None
    name: str = "i"
    processing_delay: int = 300

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class I2C(Command):
    """Set I2C address and reboot device."""

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
    """Import calibration string."""

    # TODO: implement me
    @classmethod
    def format_command(cls):
        raise NotImplementedError


class Led(Command):
    "Turn LED on/off."

    arguments: Tuple[int, int, str] = (1, 0, "?")
    name: str = "L"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: Union[int, str] = "?") -> str:
        if arg not in cls.arguments:
            raise ArgumentError(f"{arg} must be one of {cls.arguments}")
        return f"{cls.name},{arg}"


class PLock(Command):
    """Turn protocol lock on/off."""

    arguments: Tuple[int, int, str] = (1, 0, "?")
    name: str = "Plock"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: Union[int, str] = "?") -> str:
        if arg not in cls.arguments:
            raise ArgumentError(f"{arg} not one of {cls.arguments}")
        return f"{cls.name},{arg}"


class Read(Command):
    """Take a reading from a device."""

    arguments: None = None
    name: str = "R"
    processing_delay: int = 1500

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Salinity(Command):
    """Salinity compensation."""

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
    """Set temperature scale."""

    arguments: Tuple[str, str, str, str] = ("c", "k", "f", "?")
    name: str = "S"
    processing_delay: int = 300

    @classmethod
    def format_command(cls, arg: str = "c") -> str:
        if arg not in cls.arguments:
            raise ArgumentError(f"{arg} is not one of {cls.arguments}")

        return f"{cls.name},{arg}"


class Sleep(Command):
    """Put device into sleep/lower power mode."""

    arguments: None = None
    name: str = "Sleep"
    processing_delay: None = None

    @classmethod
    def format_command(cls) -> str:
        return f"{cls.name}"


class Status(Command):
    """Get status device status information."""

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
