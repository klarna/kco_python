'''Push Example

This file demonstrates the use of the Klarna library to complete
the purchase and create the order.
'''

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
# [[examples-push]]
import klarnacheckout
from uuid import uuid1

# Instance of the session library that is being used in the server
session = {}

# Instance of the HTTP library that is being used in the server
request = {}

# Shared Secret
shared_secret = 'shared_secret'

klarnacheckout.Order.content_type =\
    'application/vnd.klarna.checkout.aggregated-order-v2+json'

connector = klarnacheckout.create_connector(shared_secret)

checkout_id = request['checkout_uri']
order = klarnacheckout.Order(connector, checkout_id)
order.fetch()

if order['status'] == 'checkout_complete':
    # At this point make sure the order is created in your system and send a
    # confirmation email to the customer
    update_data = {}
    update_data['status'] = 'created'
    update_data['merchant_reference'] = {
        'orderid1': uuid1()
    }
    order.update(update_data)
# [[examples-push]]
