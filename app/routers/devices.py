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
from app.models import service, Device, DeviceParameter, DeviceOption, Job
from app.models.device import DeviceNotEnabled, SaneException, DeviceBusy


DevicesRouter = APIRouter(prefix='/devices', tags=['devices'])
OptionValue = int | float | str


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
        dev = service.get_device(device_name)
        return dev.parameters()
    except StopIteration as ex:
        raise HTTPException(404, str(ex)) from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, "Device not enabled.") from ex
    except Exception as ex:
        raise HTTPException(500, str(ex)) from ex


@DevicesRouter.get('/{device_name}/options')
async def get_device_options(device_name: str) -> List[DeviceOption]:
    """Return list of device options."""
    try:
        dev = service.get_device(device_name)
        return dev.options()
    except StopIteration as ex:
        raise HTTPException(404, f"Device {device_name} not found.") from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, "Device not enabled.") from ex


@DevicesRouter.put('/{device_name}/options')
async def set_device_options(device_name: str, option_name: str,
                             option_value: OptionValue) -> List[DeviceOption]:
    """Set a list of options."""
    try:
        dev = service.get_device(device_name)
        dev.set_option(option_name, option_value)
        return dev.options()
    except StopIteration as ex:
        raise HTTPException(404, f"Device {device_name} not found.") from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, "Device not enabled.") from ex
    except SaneException as ex:
        raise HTTPException(500, f"Internal server error: {str(ex)}") from ex
    except AttributeError as ex:
        raise HTTPException(403, f"Error setting option: {str(ex)}") from ex


@DevicesRouter.put('/{device_name}/scan')
async def scan(device_name: str) -> Job:
    """Scan using a device."""
    try:
        dev = service.get_device(device_name)
        job = dev.scan()

        return job

    except StopIteration as ex:
        raise HTTPException(404, f"Device {device_name} not found.") from ex
    except SaneException as ex:
        raise HTTPException(500, f"Internal Sane Error {str(ex)}") from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404,
                            f"Device {device_name} is not enabled.") from ex
    except DeviceBusy as ex:
        raise HTTPException(400, f"Device {device_name} is busy.") from ex


@DevicesRouter.get('/{device_name}/jobs')
async def get_jobs(device_name: str) -> List[Job]:
    """Return the list of currently available jobs run by the device."""
    try:
        dev = service.get_device(device_name)
        return dev._jobs
    except StopIteration as ex:
        raise HTTPException(404, f"Device {device_name} not found.") from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, f"Device {device_name} is not enabled.") from ex


@DevicesRouter.get('/{device_name}/jobs/{jobid}')
async def get_job(device_name: str, jobid: int) -> Job:
    """Return a job on the device."""
    try:
        dev = service.get_device(device_name)
        return dev.get_job(jobid)
    except StopIteration as ex:
        raise HTTPException(404, f"Device {device_name} not found.") from ex
    except SaneException as ex:
        raise HTTPException(500, f"Internal Sane Error {str(ex)}") from ex
    except DeviceNotEnabled as ex:
        raise HTTPException(404, f"Device {device_name} is not enabled.") from ex
    except IndexError as ex:
        raise HTTPException(404, f"Job {jobid} not found.") from ex
