###############################################################################
#  service.py for archivist scour microservice                                #
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
"""Service model."""
from typing import List
import sane
from .device import Device

SaneException = sane._sane.error


class Service():
    """Service model."""
    sane_version: str = ""
    devices: List[Device] = []

    def __init__(self):
        """Initialize the service."""
        self.sane_version = sane.init()

    def initialize(self) -> None:
        """Initialize sane service."""
        sane.exit()

        try:
            self.sane_version = sane.init()
        except SaneException as ex:
            raise ex from ex

    def refresh_devices(self) -> List[Device]:
        """Refresh the list of sane devices."""
        try:
            self.devices = list(map(lambda dev_info:
                                    Device(device_name=dev_info[0],
                                           device_model=dev_info[1],
                                           device_vendor=dev_info[2],
                                           device_type=dev_info[3]),
                                    sane.get_devices()))
        except SaneException as ex:
            raise ex from ex

        return self.devices
