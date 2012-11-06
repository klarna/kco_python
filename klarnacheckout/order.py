'''
Implementation of the order resource

Copyright 2012 Klarna AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


class Order(object):
    '''Implementation of the order resource'''

    # Base URI that is used to create order resources
    base_uri = None

    # Content Type to use
    content_type = None

    def __init__(self, data=None):
        '''Create a new Order object

        `data` Initial data
        '''

        self._location = None
        self._data = {} if data is None else dict(data)

    def __getitem__(self, key):
        '''Getter mapping'''

        return self._data[key]

    def __setitem__(self, key, value):
        '''Setter mapping'''

        self._data[key] = value

    def keys(self):
        '''Key '''

        return self._data.keys()

    @property
    def location(self):
        '''URI of remote resource'''
        return self._location

    @location.setter
    def location(self, location):
        self._location = str(location)

    def get_content_type(self):
        '''Return content type of the resource'''
        return self.content_type

    def parse(self, data):
        '''Replace resource data

        `data` data
        '''

        self._data = dict(data)

    def marshal(self):
        '''Basic representation of the object'''

        return dict(self._data)

    def create(self, connector):
        '''Create a new order

        `connector` An instance of connector class
        '''

        options = {"url": self.base_uri}
        connector.apply("POST", self, options)

    def fetch(self, connector, location=None):
        '''Fetch order data

        `connector` An instance of connector class
        `location` optional uri
        '''

        if location:
            self.location = location
        options = {"url": self._location}

        connector.apply("GET", self, options)

    def update(self, connector, location=None):
        '''Update order data

        `connector` An instance of connector class
        `location` optional uri
        '''

        if location:
            self.location = location
        options = {"url": self._location}

        connector.apply("POST", self, options)
