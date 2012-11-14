'''Checkout example

This file demonstrates the use of the Klarna library to display the checkout
'''

# Copyright 2012 Klarna AB
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

# Instance of the session library that is being used in the server
session = {}

# Dictionary containing the cart items
cart = (
    {
        'quantity': 1,
        'reference': 'BANAN01',
        'name': 'Bananana',
        'unit_price': 450,
        'discount_rate': 0,
        'tax_rate': 2500
    }, {
        'quantity': 1,
        'type': 'shipping_fee',
        'reference': 'SHIPPING',
        'name': 'Shipping Fee',
        'unit_price': 450,
        'discount_rate': 0,
        'tax_rate': 2500
    }
)

# Merchant ID
eid = "2"

# Shared Secret
shared_secret = 'shared_secret'

klarnacheckout.Order.base_uri = \
    'https://klarnacheckout.apiary.io/checkout/orders'
klarnacheckout.Order.content_type =\
    'application/vnd.klarna.checkout.aggregated-order-v2+json'

connector = klarnacheckout.create_connector(shared_secret)

order = None

if 'klarna_checkout' in session:
    # Resume session
    order = klarnacheckout.Order(connector, session["klarna_checkout"])
    try:
        order.fetch()

        update_data = {}
        update_data["cart"] = {}

        # Reset cart
        update_data["cart"]["items"] = []
        for item in cart:
            update_data["cart"]["items"].append(item)

        order.update(update_data)
    except:
        # Reset session
        order = None
        del session["klarna_checkout"]


if order is None:
    create_data = {}

    # Start new session
    create_data['purchase_country'] = 'SE'
    create_data['purchase_currency'] = 'SEK'
    create_data['locale'] = 'sv-se'
    create_data['merchant'] = {
        'id': eid,
        'terms_uri': 'http://localhost/terms.html',
        'checkout_uri': 'http://localhost/checkout',
        # You can not receive push notification on
        # non publicly available uri
        'confirmation_uri': 'http://localhost/confirmation',
        'push_uri': 'http://localhost/push'
    }
    create_data["cart"] = {"items": []}

    for item in cart:
        create_data["cart"]["items"].append(item)

    order = klarnacheckout.Order(connector)
    order.create(create_data)
    order.fetch()

# Store location of checkout session
session["klarna_checkout"] = order.location

# Display checkout
print "<div>%s</div>" % (order["gui"]["snippet"])
