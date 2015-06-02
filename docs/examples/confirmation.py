# -*- coding: UTF-8 -*-
'''Confirmation Example

This file demonstrates the use of the Klarna library to complete
the purchase and display the confirmation page snippet.
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

# Instance of the session library that is being used in the server
session = {}

shared_secret = 'shared_secret'

connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)

order_id = session['klarna_order_id']

try:
	order = klarnacheckout.Order(connector, order_id)
	order.fetch()
except klarnacheckout.HTTPResponseException as e:
    print(e.json.get('http_status_message'))
    print(e.json.get('internal_message'))
    sys.exit()

if order['status'] != 'checkout_complete':
    raise Exception('Checkout not completed, redirect to checkout.py')

# Display confirmation
snippet = u'<div>%s</div>' % (order['gui']['snippet'])

if not isinstance(snippet, str):
    snippet = snippet.encode('utf-8')

print(snippet)


del session['klarna_order_id']
