'''Implementation of the base resource'''

# Copyright 2013 Klarna AB
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


class Resource(object):
    '''Base resource'''

    # Connector
    connector = None

    def __init__(self, connector, uri=None):
        '''Create a new Order object

        `connector` connector to use
        `uri` uri of resource
        '''
        self.connector = connector
        self._location = None
        self._data = {}
        if uri:
            self._location = uri

    def __getitem__(self, key):
        '''Getter mapping'''
        return self._data[key]

    def __setitem__(self, key, value):
        '''Setter mapping'''
        self._data[key] = value

    def keys(self):
        '''Key '''
        return self._data.keys()

    def __iter__(self):
        '''Iter'''
        return self._data.__iter__()

    @property
    def accept(self):
        '''Accepted content type to request'''
        return self.content_type

    @property
    def location(self):
        '''URI of remote resource'''
        return self._location

    @location.setter
    def location(self, location):
        self._location = str(location)

    def parse(self, data):
        '''Replace resource data

        `data` data
        '''
        self._data = dict(data)

    def marshal(self):
        '''Basic representation of the object'''
        return dict(self._data)

    def __repr__(self):
        return '<Order %r>' % (self._location,)
