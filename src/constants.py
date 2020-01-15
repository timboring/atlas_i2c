from typing import Dict

import commands

command_mapping: Dict = {
    "baud": commands.Baud,
    "calibrate": commands.Calibrate,
    "export": commands.Export,
    "factory": commands.Factory,
    "find": commands.Find,
    "info": commands.Info,
    "i2c": commands.I2C,
    "import": commands.Import,
    "led": commands.LED,
    "plock": commands.PLock,
    "read": commands.Read,
    "sleep": commands.Sleep,
    "status": commands.Status,
    "salinity": commands.Salinity,
    "scale": commands.Scale,
}

status_code: Dict = {1: "SUCCESS", 2: "SYNTAX ERROR", 254: "NOT READY", 255: "NO DATA TO SEND"}
