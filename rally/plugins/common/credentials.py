# Copyright 2016: Mirantis Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import jsonschema
import six

from rally.common.plugin import plugin


def configure(name, schema):
    """Credentials class wrapper.

    Each credentials class has to be wrapped by configure() wrapper.
    It sets essential configuration of credentials classes.
    Actually this wrapper just adds attributes to the class.

    :param name: Name of the class, used in credentials type field
    :param schema: Json schema to validate on initialization
    """
    def wrapper(cls):
        cls = plugin.configure(name=name)(cls)
        cls._meta_set("schema", schema)
        return cls

    return wrapper


@six.add_metaclass(abc.ABCMeta)
@configure(name="base_credentials", schema=None)
class Credentials(plugin.Plugin):
    """Base credentials plugin."""
    def __init__(self, credentials):
        self.validate(credentials)
        super(Credentials, self).__setattr__("credentials", credentials)

    def __getattr__(self, item):
        try:
            if item in self.__dict__:
                return self.__dict__[item]
            return self.credentials[item]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        self.credentials[key] = value

    def to_dict(self):
        return self.credentials.copy()

    def validate(self, obj):
        jsonschema.validate(obj, self._meta_get("schema"))
