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
"""Backend service routes."""

from typing import Union, List
from fastapi import APIRouter, HTTPException
from app.models import service, Device

ServiceRouter = APIRouter(prefix='/service', tags=['service'])


@ServiceRouter.get('')
async def get_service():
    """Return information about the microservice configuration."""
    try:
        return service.sane_version
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@ServiceRouter.get('/devices')
async def devices():
    """Get a list of devices through sane."""
    try:
        return service.devices
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@ServiceRouter.get('/refresh_devices')
async def refresh_devices() -> List[Device]:
    """Refresh list of available devices."""
    try:
        return service.refresh_devices()
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@ServiceRouter.put('/discover')
async def discover_device(url: str, name: str) -> List[Device]:
    """Discover a new scanning device."""
    try:
        return service.refresh_devices()
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@ServiceRouter.put('/configure/{device_name}')
async def configure_device(device_name: str, option: Union[str, None],
                           value: Union[str, None]):
    """Set default for a scanning device."""
    raise HTTPException(500, "Not Implemented")


@ServiceRouter.put('/reinitialize')
async def reinitialize():
    """Reinitialize sane backend."""
    raise HTTPException(500, "Not Implemented")
