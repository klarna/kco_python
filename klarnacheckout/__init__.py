'''Checkout API wrapper'''

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

from .useragent import UserAgent, __version__
from .connector import Connector
from .order import Order
from .digest import create_digester

__all__ = ('create_connector', Connector, Order)


def create_connector(secret):
    '''Create a new `Connector` with the default configiruation'''

    return Connector(
        UserAgent(),
        create_digester(secret))
