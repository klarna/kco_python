'''Checkout order resource'''

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

from .resource import Resource


class Order(Resource):
    '''Checkout order resource'''

    # Base URI that is used to create order resources
    relative_uri = '/checkout/orders'

    # Content Type to use
    content_type = 'application/vnd.klarna.checkout.aggregated-order-v2+json'

    def __init__(self, connector, id=None):
        '''Create a new Order object

        `connector` connector to use
        `id` order id to use
        '''
        super(Order, self).__init__(connector)
        if id:
            self.location = connector.base + self.relative_uri + '/' + id

    def create(self, data):
        '''Create a new order

        `data` Data to initialise order resource with
        '''
        options = {"url": self.connector.base + self.relative_uri,
                   "data": data}
        self.connector.apply("POST", self, options)

    def fetch(self):
        '''Fetch order data'''
        options = {"url": self._location}
        self.connector.apply("GET", self, options)

    def update(self, data):
        '''Update order data

        `data` data to update order resource with
        '''
        options = {"url": self._location,
                   "data": data}
        self.connector.apply("POST", self, options)
