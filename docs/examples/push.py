# -*- coding: UTF-8 -*-
'''Push Example

This file demonstrates the use of the Klarna library to complete
the purchase and create the order.
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
import klarnacheckout
import sys
from uuid import uuid1

# Instance of the session library that is being used in the server
session = {}

# Instance of the HTTP library that is being used in the server
request = {}

# Shared Secret
shared_secret = 'shared_secret'

connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)

checkout_uri = request['klarna_order']

try:
    order = klarnacheckout.Order(connector, checkout_uri)
    order.fetch()
except klarnacheckout.HTTPResponseException as e:
    print(e.json.get('http_status_message'))
    print(e.json.get('internal_message'))

    sys.exit()

if order['status'] == 'checkout_complete':
    # At this point make sure the order is created in your system and send a
    # confirmation email to the customer
    update_data = {}
    update_data['status'] = 'created'
    update_data['merchant_reference'] = {
        'orderid1': str(uuid1())
    }

    try:
        order.update(update_data)
    except klarnacheckout.HTTPResponseException as e:
        print(e.json.get('http_status_message'))
        print(e.json.get('internal_message'))
