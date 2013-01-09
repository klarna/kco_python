'''Fetch example

This file demonstrates the use of the Klarna library to fetch an order.
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
# [[examples-fetch]]
import klarnacheckout

# Shared Secret
shared_secret = 'shared_secret'

klarnacheckout.Order.content_type = \
    'application/vnd.klarna.checkout.aggregated-order-v2+json'

resource_location = \
    'https://checkout.testdrive.klarna.com/checkout/orders/ABC123'

connector = klarnacheckout.create_connector(shared_secret)

order = klarnacheckout.Order(connector, resource_location)

order.fetch()
# [[examples-fetch]]
