###############################################################################
#  device.py for archivist scour microserver                                  #
# Copyright (c) 2024 Tom Hartman (thomas.lees.hartman@gmail.com)              #
#                                                                             #
#  This program is free software; you can redistribute it and/or              #
#  modify it under the terms of the GNU General Public License                #
#  as published by the Free Software Foundation; either version 2             #
#  of the License, or the License, or (at your option) any later              #
#  version.                                                                   #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
###############################################################################
"""Device classes."""
from enum import IntEnum
from typing import List, Tuple
import sane
from pydantic import BaseModel

SaneException = sane._sane.error


class DevParams(IntEnum):
    """Sane device parameters."""

    FORMAT = 0
    LAST_FRAME = 1
    RESOLUTION = 2
    DEPTH = 3
    BYTES_PER_LINE = 4


class DevStatus(IntEnum):
    """Sane device statuses."""

    DISABLED = 0
    ENABLED = 1
    SCANNING = 2
    COMPLETED = 3
    ERROR = 4


class DeviceNotEnabled(Exception):
    """Raise when a device is not enabled and operations are performed."""


class DeviceSaneException(Exception):
    """Raised when there is an internal sane exception."""


class DeviceParameter(BaseModel):
    """Device parameter model."""

    device_format: str
    last_frame: int
    pixelPerLine: int
    lines: int
    depth: int
    bytes_per_line: int


class DeviceOption(BaseModel):
    """Device option model."""

    name: str
    description: str
    value: str | int
    py_name: str
    option_type: int
    unit: int
    size: int
    cap: int
    constaints: None | Tuple[int, int, int] | List[str | int]


class Device(BaseModel):
    """Device model."""

    device_name: str
    device_model: str
    device_vendor: str
    device_type: str

    _sane_dev: object = None

    def __del__(self) -> None:
        """Destructor for a sane device."""
        if self._sane_dev is not None:
            self._sane_dev.close()

    def enable(self) -> None:
        """Enable sane device."""
        try:
            self._sane_dev = sane.open(self.device_name)
        except SaneException as ex:
            raise ex from ex

    def parameters(self) -> DeviceParameter:
        """Return the list of device parameters."""
        if self._sane_dev is None:
            raise DeviceNotEnabled()

        try:
            params = self._sane_device.get_parameters()
        except SaneException as ex:
            raise DeviceSaneException(str(ex)) from ex

        return DeviceParameter(device_format=params[DevParams.FORMAT],
                               last_frame=params[DevParams.LAST_FRAME],
                               pxielPerLine=params[DevParams.RESOLUTION][0],
                               lines=params[DevParams.RESOLUTION][1],
                               depth=params[DevParams.DEPTH],
                               bytes_per_line=params[DevParams.BYTES_PER_LINE])

    def options(self) -> List[DeviceOption]:
        """Return the current options for a device."""
        if self._sane_dev is None:
            raise DeviceNotEnabled()

        try:
            dev = self._sane_dev
            opt_names = list(filter(lambda opt: opt != 'None',
                                    list(dev.opt.keys())))
            opts = list(map(lambda opt:
                            DeviceOption(name=dev[opt].name,
                                         description=dev[opt].desc,
                                         value=getattr(dev, opt),
                                         py_name=dev[opt].py_name,
                                         option_type=dev[opt].type,
                                         unit=dev[opt].unit,
                                         size=dev[opt].size,
                                         cap=dev[opt].cap,
                                         constraints=dev[opt].constraints),
                            opt_names))
        except SaneException as ex:
            raise DeviceSaneException(str(ex)) from ex

        return opts
