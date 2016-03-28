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

from rally import consts
from rally.plugins.common import credentials


openstack_credentials_schema = {

    "type": "object",

    "properties": {
        "auth_url": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
        "tenant_name": {"type": ["string", "null"]},
        "permission": {"type": ["string", "null"]},
        "region_name": {"type": ["string", "null"]},
        "endpoint_type": {"type": ["string", "null"]},
        "domain_name": {"type": ["string", "null"]},
        "user_domain_name": {"type": ["string", "null"]},
        "admin_domain_name": {"type": ["string", "null"]},
        "project_domain_name": {"type": ["string", "null"]},
        "endpoint": {"type": ["string", "null"]},
        "https_insecure": {"type": "boolean"},
        "https_cacert": {"type": ["string", "null"]},
    },
    "required": ["auth_url", "username", "password"],

    "additionalProperties": False
}

default_credentials_values = {
    "tenant_name": None,
    "permission": consts.EndpointPermission.USER,
    "region_name": None,
    "endpoint_type": consts.EndpointType.PUBLIC,
    "domain_name": None,
    "endpoint": None,
    "user_domain_name": "Default",
    "admin_domain_name": "Default",
    "project_domain_name": "Default",
    "https_insecure": False,
    "https_cacert": None
}


@credentials.configure(name="openstack", schema=openstack_credentials_schema)
class OpenStackCredentials(credentials.Credentials):
    """OpenStack credentials plugin."""

    def __init__(self, credentials_dict):
        # NOTE(rpromyshlennikov): it needs to mix input values
        # with default values to save backward compatibility
        # with old Credentials class
        credentials_with_default = default_credentials_values.copy()
        credentials_with_default.update(credentials_dict)
        super(OpenStackCredentials, self).__init__(credentials_with_default)
        self.insecure = self.https_insecure
        self.cacert = self.https_cacert

    def to_dict(self, include_permission=False):
        credentials_dict = self.credentials.copy()
        credentials_dict.pop("cacert")
        credentials_dict.pop("insecure")
        if not include_permission:
            credentials_dict.pop("permission")
        return credentials_dict
