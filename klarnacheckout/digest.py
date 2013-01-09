'''Digester'''

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

import hashlib
from base64 import b64encode


def create_digester(secret):
    '''Creates a digest function that hashes a string using the given secret

    `secret` shared secret
    '''

    secret = secret.encode('utf-8')

    def digester(string):
        '''Creates a digest hash'''
        hash = hashlib.sha256()
        if string:
            hash.update(string)
        hash.update(secret)
        return b64encode(hash.digest()).decode('utf-8')

    return digester
