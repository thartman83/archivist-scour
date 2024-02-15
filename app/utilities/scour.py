###############################################################################
#  scour.py for archivist scour microservice                                  #
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
"""Sane functional wrapper."""

import sane
from pydantic import BaseModel

SaneException = sane._sane.error


class ScourSaneException(Exception):
    """Sane error."""


class ScourDevice(BaseModel):
    """Base model for sane devices."""

    _sane_dev: object

    def __init__(self, sane_dev) -> None:
        """Constructor for ScourDevice model."""
        self._sane_dev = sane_dev
        super().__init__()

    def __del__(self) -> None:
        """Destructor for ScourDevice model."""
        self._sane_dev.disable()

    def enable(self) -> None:
        """Enable a sane device."""
        try:
            self._sane_dev.enable()
        except SaneException as ex:
            raise ScourSaneException(str(ex)) from ex


class Scour(BaseModel):
    """Base model for sane."""

    initialized: bool
    sane_version: str
    sane_devices: list

    def __init__(self) -> str:
        """Constructor for Scour Object."""
        self.sane_devices = []
        self.sane_version = ""
        self.initialized = True
        super().__init__()

    def initialize(self) -> None:
        """Initialize the sane backend."""
        sane.exit()

        try:
            self.sane_version = sane.init()
        except SaneException as ex:
            raise ScourSaneException(str(ex)) from ex

        return self.sane_version

    def refresh_devices(self) -> list[ScourDevice]:
        """Retrieve a new set of devices from sane."""


# return the scour singleton
scour = Scour()
