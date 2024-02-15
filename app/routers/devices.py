###############################################################################
#  devices.py for archivist scour microservice                                #
#  Copyright (c) 2024 Tom Hartman (thomas.lees.hartman@gmail.com)             #
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
"""Device routes."""

from typing import List
from fastapi import APIRouter, HTTPException
from app.models import service, Device, DeviceParameter
from app.models.device import DeviceNotEnabled

DevicesRouter = APIRouter(prefix='/devices', tags=['devices'])


@DevicesRouter.get('')
async def get_devices() -> List[Device]:
    """Return the list of available devices."""
    try:
        return service.devices
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@DevicesRouter.get('/{device_name}/parameters')
async def get_device_parameters(device_name: str) -> DeviceParameter:
    """Return the devices parameters."""
    try:
        dev = next(d for d in service.devices if d.device_name == device_name)
        return dev.parameters()
    except StopIteration as ex:
        raise HTTPException(404, str(ex)) from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, "Device not enabled.") from ex
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex
