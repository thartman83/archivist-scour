###############################################################################
#  test_device_model.py for archivist scour microservice                      #
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
"""Unit tests for device model."""
from app.models import Device
from app.models import Job
from PIL import Image


def test_get_next_job_id():
    """
    GIVEN a device object
    WHEN get_next_job_id is called
    SHOULD return the next id.
    """
    device = Device(device_name="brother4:net1;dev0",
                    device_model="Brother",
                    device_vendor="*Brother",
                    device_type="L2700DW")
    jobid = device._get_next_jobid()

    assert jobid == 0


def test_job_pages():
    """
    GIVEN a Job object
    WHEN a page is added
    SHOULD serialize.
    """
    job = Job(job_number=1)
    job.add_pages(Image.open('tests/data/lorem1.png'))

    job.model_dump()
