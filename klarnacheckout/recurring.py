'''Resources for dealing with recurring orders'''

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


class RecurringOrder(Resource):
    '''Recurring order resource'''

    # Base URI that is used to create recurring order resources
    relative_uri = '/checkout/recurring/%s/orders'

    # Content Type to use
    content_type = 'application/vnd.klarna.checkout.recurring-order-v1+json'

    # Accept type to use
    accept = 'application/vnd.klarna.checkout.recurring-order-accepted-v1+json'

    def __init__(self, connector, token):
        '''Create a new RecurringOrder object

        `connector` connector to use
        `token` recurring token to use
        '''
        super(RecurringOrder, self).__init__(connector)
        self.location = connector.base + self.relative_uri % token

    def create(self, data):
        '''Create a new order

        `data` Data to initialise order resource with
        '''
        options = {"url": self._location,
                   "data": data}
        self.connector.apply("POST", self, options)


class RecurringStatus(Resource):
    '''Recurring order status resource'''

    # Base URI that is used to fetch recurring status
    relative_uri = '/checkout/recurring/%s'

    # Content Type to use
    content_type = 'application/vnd.klarna.checkout.recurring-status-v1+json'

    def __init__(self, connector, token):
        '''Create a new RecurringStatus object

        `connector` connector to use
        `token` recurring token to use
        '''
        super(RecurringStatus, self).__init__(connector)
        self.location = connector.base + self.relative_uri % token

    def fetch(self):
        '''Fetch order data'''
        options = {"url": self._location}
        self.connector.apply("GET", self, options)
