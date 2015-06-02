# -*- coding: UTF-8 -*-
'''Fetch recurring order example

This file demonstrates the use of the Klarna library to fetch the status of a
recurring order.

Note! First you must have created a regular aggregated order with the option
"recurring" set to true.  After that order has received either status
"checkout_complete" or "created" you can fetch that resource and retrieve the
"recurring_token" property which is needed to create recurring orders.
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

shared_secret = 'shared_secret'
recurring_token = 'ABC123'

connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)

try:
    recurring_status = klarnacheckout.RecurringStatus(connector, recurring_token)
    recurring_status.fetch()

    print(str(recurring_status) + ' : %s' % recurring_status['payment_method']);
except klarnacheckout.HTTPResponseException as e:
    print(e.json.get('http_status_message'))
    print(e.json.get('internal_message'))
