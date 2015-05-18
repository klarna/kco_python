# -*- coding: UTF-8 -*-
'''Fetch example

This file demonstrates the use of the Klarna library to fetch an order.
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

# Shared Secret
shared_secret = 'shared_secret'

location = 'https://checkout.testdrive.klarna.com/checkout/orders/ABC123'

connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)

try:
    order = klarnacheckout.Order(connector, location)
    order.fetch()
except klarnacheckout.HTTPResponseException as e:
    print(e.json.get('http_status_message'))
    print(e.json.get('internal_message'))
