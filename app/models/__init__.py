###############################################################################
#  __init__.py for archivist scour microservice                               #
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
"""Entry point for models module."""

import sane
from .service import Service
from .device import Device, DeviceParameter, DeviceOption
from .job import Job, JobStatus

SaneException = sane._sane.error

service = Service()

__all__ = ["service", "Device", "DeviceParameter", "DeviceOption",
           "SaneException", "Job", "JobStatus"]
