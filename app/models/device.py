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
from threading import Thread
from enum import IntEnum
from typing import List, Tuple
import sane
from pydantic import BaseModel
from .job import Job, JobStatus

SaneException = sane._sane.error

OptionConstraint = None | List[str | int | float] | Tuple[int | float]


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
    IDLE = 1
    SCANNING = 2
    ERROR = 4


class OptionType(IntEnum):
    """Sane device option types."""

    TYPE_BOOL = 0
    TYPE_INT = 1
    TYPE_FIXED = 2
    TYPE_STRING = 3
    TYPE_BUTTON = 4
    TYPE_GROUP = 5


class DeviceNotEnabled(Exception):
    """Raise when a device is not enabled and operations are performed."""


class DeviceSaneException(Exception):
    """Raised when there is an internal sane exception."""


class DeviceBusy(Exception):
    """Raised when the device is unable to perform an action
    because it is busy."""


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
    active: bool
    value: str | int | float | None
    py_name: str
    option_type: int
    unit: int
    size: int
    cap: int
    constraint: OptionConstraint


class Device(BaseModel):
    """Device model."""

    device_name: str
    device_model: str
    device_vendor: str
    device_type: str
    device_status: DevStatus = DevStatus.DISABLED

    _sane_dev: object = None
    _current_job: Job = None
    _jobs: List[Job] = []
    _max_jobs: int = 10

    def __del__(self) -> None:
        """Destructor for a sane device."""
        if self._sane_dev is not None:
            self._sane_dev.close()

    def enable(self) -> DevStatus:
        """Enable sane device."""
        try:
            if self.device_status == DevStatus.DISABLED:
                self._sane_dev = sane.open(self.device_name)
                self.device_status = DevStatus.IDLE

            return self.device_status

        except SaneException as ex:
            raise ex from ex

    def disable(self) -> DevStatus:
        """Disable a sane device."""
        try:
            if self.device_status == DevStatus.IDLE:
                self._sane_dev.close()
                self.device_status = DevStatus.DISABLED
            else:
                raise DeviceBusy()
            return self.device_status
        except SaneException as ex:
            raise ex from ex

    def parameters(self) -> DeviceParameter:
        """Return the list of device parameters."""
        if self._sane_dev is None:
            raise DeviceNotEnabled()

        try:
            parms = self._sane_dev.get_parameters()
            return DeviceParameter(device_format=parms[DevParams.FORMAT],
                                   last_frame=parms[DevParams.LAST_FRAME],
                                   pixelPerLine=parms[DevParams.RESOLUTION][0],
                                   lines=parms[DevParams.RESOLUTION][1],
                                   depth=parms[DevParams.DEPTH],
                                   bytes_per_line=parms[DevParams.BYTES_PER_LINE])

        except SaneException as ex:
            raise DeviceSaneException(str(ex)) from ex

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
                                         active=dev[opt].is_active() == 1,
                                         value=getattr(dev, opt) if
                                         dev[opt].is_active() else None,
                                         py_name=dev[opt].py_name,
                                         option_type=dev[opt].type,
                                         unit=dev[opt].unit,
                                         size=dev[opt].size,
                                         cap=dev[opt].cap,
                                         constraint=dev[opt].constraint),
                            opt_names))
            return opts
        except SaneException as ex:
            raise DeviceSaneException(str(ex)) from ex

        return opts

    def set_option(self, option_name: str, option_value: str) -> None:
        """Set a device option."""
        if self._sane_dev is None:
            raise DeviceNotEnabled()

        try:
            opts = self.options()
            opt = next(o for o in opts if o.py_name == option_name)
            value = option_value
            if opt.option_type in [OptionType.TYPE_BOOL, OptionType.TYPE_INT]:
                value = int(option_value)
            elif opt.option_type == OptionType.TYPE_FIXED:
                value = float(option_value)

            setattr(self._sane_dev, option_name, value)
        except SaneException as ex:
            raise ex from ex
        except AttributeError as ex:
            raise ex from ex

    def scan(self) -> Job:
        """Use the device to scan."""
        if self._sane_dev is None:
            raise DeviceNotEnabled()

        if self.device_status is not DevStatus.IDLE:
            raise DeviceBusy()

        self._current_job = Job(job_number=self._get_next_jobid())
        self._jobs.append(self._current_job)

        Thread(target=self._start_scan).start()

        return self._current_job

    def get_job(self, jobid: int) -> Job:
        """Return a scan job from the device."""
        return self._jobs[jobid]

    def _get_next_jobid(self) -> int:
        """Return the next available job id."""
        return len(self._jobs)

    def _start_scan(self) -> None:
        """Private method to do the actual scanning."""
        try:
            self.device_status = DevStatus.SCANNING
            source = next(o for o in self.options() if
                          o.py_name == 'source')

            if source.value.lower() == 'flatbed':
                page = self._sane_dev.scan()
                self._current_job.add_pages(page)
            else:
                pages = self._sane_dev.multi_scan()
                for page in pages:
                    self._current_job.add_pages(page)
            self.device_status = DevStatus.IDLE
            self._current_job.status = JobStatus.COMPLETED
        except SaneException as ex:
            self.device_status = DevStatus.ERROR
            self._current_job.status = JobStatus.ERROR
            raise ex from ex
        except StopIteration as ex:
            raise ex from ex
