###############################################################################
#  job.py for archivist scour microservice                                    #
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

"""Model for a scour scan job."""
from base64 import b64encode
from io import BytesIO
from enum import IntEnum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Base64Bytes
from PIL import Image


class JobStatus(IntEnum):
    """Sane job statuses."""

    STARTED = 0
    COMPLETED = 1
    ERROR = 2


class Job(BaseModel):
    """Model for a scan job."""

    job_number: int
    pages: List[Base64Bytes] = []
    start_date: datetime = datetime.now()
    end_date: datetime = None
    status: JobStatus = JobStatus.STARTED
    error: str = ""
    _pages: List[Image] = []

    def add_pages(self, page: Image) -> None:
        """Add pages to the job."""
        self._pages.append(page)
        buf = BytesIO()
        page.save(buf, format='JPEG')
        self.pages.append(b64encode(buf.getvalue()))
