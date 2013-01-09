'''Create example

This file demonstrates the use of the Klarna library to create an order.
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
# [[examples-create]]
import klarnacheckout

# Dictionary containing the cart items
cart = (
    {
        'quantity': 1,
        'reference': '123456789',
        'name': 'Klarna t-shirt',
        'unit_price': 12300,
        'discount_rate': 1000,
        'tax_rate': 2500
    }, {
        'quantity': 1,
        'type': 'shipping_fee',
        'reference': 'SHIPPING',
        'name': 'Shipping Fee',
        'unit_price': 4900,
        'tax_rate': 2500
    }
)

# Merchant ID
eid = "0"

# Shared Secret
shared_secret = 'shared_secret'


klarnacheckout.Order.base_uri = \
    'https://checkout.testdrive.klarna.com/checkout/orders'
klarnacheckout.Order.content_type = \
    'application/vnd.klarna.checkout.aggregated-order-v2+json'

connector = klarnacheckout.create_connector(shared_secret)

order = None

merchant = {
    'id': eid,
    'terms_uri': 'http://example.com/terms.html',
    'checkout_uri': 'http://example.com/checkout',
    'confirmation_uri': ('http://example.com/thank-you' +
                         '?sid=123&klarna_order={checkout.order.uri}'),
    # You can not receive push notification on
    # a non publicly available uri
    'push_uri': ('http://example.com/push' +
                 '?sid=123&klarna_order={checkout.order.uri}')
}

data = {
    'purchase_country': 'SE',
    'purchase_currency': 'SEK',
    'locale': 'sv-se',
    'merchant': merchant
}
data["cart"] = {"items": []}

for item in cart:
    data["cart"]["items"].append(item)

order = klarnacheckout.Order(connector)
order.create(data)

# [[examples-create]]
