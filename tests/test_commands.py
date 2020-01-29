import pytest

from atlas_i2c import commands


class TestBaudCommand:
    @pytest.mark.parametrize("arg", [300, 1200, 2400, 9600, 19200, 38400, 57600, 115200])
    def test_format_command(self, arg):
        baud = commands.Baud
        cmd = baud.format_command(arg)
        assert cmd == f"{baud.name},{arg}"

    @pytest.mark.parametrize("arg", ["300", "foo"])
    def test_format_command_with_invalid_arg(self, arg):
        with pytest.raises(commands.ArgumentError):
            commands.Baud.format_command(arg)


class TestDataLoggerCommand:
    @pytest.mark.parametrize("arg", [0, 10, 5000, 32000, "?"])
    def test_format_command(self, arg):
        data_logger = commands.DataLogger
        cmd = data_logger.format_command(arg)
        assert cmd == f"{data_logger.name},{arg}"

    @pytest.mark.parametrize("arg", [-1, 32001, "!"])
    def test_format_command_with_invalid_arg(self, arg):
        with pytest.raises(commands.ArgumentError):
            commands.DataLogger.format_command(arg)


class TestFactoryCommand:
    def test_format_command(self):
        assert commands.Factory.format_command() == f"{commands.Factory.name}"

    def test_format_command_with_arg(self):
        with pytest.raises(TypeError):
            commands.Factory.format_command("foo")


class TestLedCommand:
    @pytest.mark.parametrize("arg", [1, 0, "?"])
    def test_format_command(self, arg):
        led = commands.Led
        cmd = led.format_command(arg)
        assert cmd == f"{led.name},{arg}"

    @pytest.mark.parametrize("arg", [-1, 2, "!"])
    def test_format_command_with_invalid_arg(self, arg):
        with pytest.raises(commands.ArgumentError):
            commands.Led.format_command(arg)


class TestPLockCommand:
    @pytest.mark.parametrize("arg", [1, 0, "?"])
    def test_format_command(self, arg):
        assert commands.PLock.format_command(arg) == f"{commands.PLock.name},{arg}"

    @pytest.mark.parametrize("invalid_arg", ["1,0,?", 2, "1,?", "0,?", "10?"])
    def test_format_command_with_invalid_args(self, invalid_arg):
        with pytest.raises(commands.ArgumentError):
            commands.PLock.format_command(invalid_arg)


class TestSalinityCommand:
    def test_format_command_without_args(self):
        with pytest.raises(commands.ArgumentError):
            assert commands.Salinity.format_command()

    def test_format_command_with_value(self):
        assert commands.Salinity.format_command(value=5) == f"{commands.Salinity.name},5"

    def test_format_command_with_value_ppt(self):
        assert (
            commands.Salinity.format_command(value=5, ppt=True) == f"{commands.Salinity.name},5,ppt"
        )

    def test_format_command_with_question(self):
        assert commands.Salinity.format_command(question=True) == f"{commands.Salinity.name},?"


class TestScaleCommand:
    @pytest.mark.parametrize("arg", ["c", "k", "f", "?"])
    def test_format_command(self, arg):
        assert commands.Scale.format_command(arg) == f"{commands.Scale.name},{arg}"

    @pytest.mark.parametrize("invalid_arg", ["c,k,f,?", "z", 1, "foo"])
    def test_format_command_with_invalid_args(self, invalid_arg):
        with pytest.raises(commands.ArgumentError):
            commands.Scale.format_command(invalid_arg)
