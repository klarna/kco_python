'''Confirmation Example

This file demonstrates the use of the Klarna library to complete
the purchase and display the confirmation page snippet.
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
# [[examples-confirmation]]
import klarnacheckout

# Instance of the session library that is being used in the server
session = {}

# Shared Secret
shared_secret = 'shared_secret'

klarnacheckout.Order.content_type =\
    'application/vnd.klarna.checkout.aggregated-order-v2+json'

connector = klarnacheckout.create_connector(shared_secret)

checkout_id = session['klarna_checkout']
order = klarnacheckout.Order(connector, checkout_id)
order.fetch()

if order['status'] != 'checkout_complete':
    raise Exception('Checkout not completed, redirect to checkout.py')

print "<div>%s</div>" % (order["gui"]["snippet"])
del session['klarna_checkout']
# [[examples-confirmation]]
