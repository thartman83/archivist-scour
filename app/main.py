###############################################################################
#  main.py for archivist scour microservice                                   #
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
"""Main enrty point for fastapi microservice."""

from fastapi import FastAPI
from .routers import ServiceRouter, DevicesRouter

app = FastAPI(title="Scour", version="0.0.1")
app.include_router(ServiceRouter)
app.include_router(DevicesRouter)
