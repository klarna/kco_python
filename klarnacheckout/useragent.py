'''UserAgent

Generates a nicely formatted user agent string containing some general system
information and the version of this library.

Additional fields can be added with the formatting taken care of.
'''

# Copyright 2015 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os

__version__ = '3.0.1'


class UserAgent(object):
    '''UserAgent string builder Class'''

    def __init__(self):
        '''Initialise user-agent with default fields'''

        pimp = ''
        if hasattr(sys, "implementation"):
            pimp = sys.implementation.name
        else:
            pimp = sys.subversion[0]

        # Components of the user-agent
        self._fields = {
            "Library": {
                "name": "Klarna.ApiWrapper",
                "version": __version__
            },
            "OS": {
                "name": os.uname()[0],
                "version": os.uname()[2]
            },
            "Language": {
                "name": "Python",
                "version": ".".join(map(str, sys.version_info[:3])),
                "options": [pimp]
            }
        }

    def add_field(self, field, data):
        '''Add a new field to the user agent

        `field` Name of field
        `data` data dictionary with name, version and possibly options
        '''

        field = str(field)
        if field in self._fields:
            raise ValueError("Unable to redefine field %s" % (field))

        self._fields[field] = dict(data)

    def __str__(self):
        '''Serialise fields to a user agent string'''

        parts = []
        for (key, value) in self._fields.items():
            parts.append("%s/%s_%s" % (key, value["name"], value["version"]))
            if "options" in value:
                parts.append("(%s)" % (" ; ".join(value["options"])))

        return " ".join(parts)
