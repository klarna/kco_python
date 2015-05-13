# -*- coding: UTF-8 -*-
'''Fetch recurring order example

This file demonstrates the use of the Klarna library to fetch the status of a
recurring order.
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

import klarnacheckout

# Shared Secret
shared_secret = 'shared_secret'

# Recurring order token
token = 'abc123'

connector = klarnacheckout.create_connector(shared_secret,
                                            klarnacheckout.BASE_TEST_URL)

try:
    order = klarnacheckout.RecurringStatus(connector, token)
    order.fetch()
except klarnacheckout.HTTPResponseException as e:
    print(e.json.get('http_status_message'))
    print(e.json.get('internal_message'))
