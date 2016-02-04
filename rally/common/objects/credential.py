# Copyright 2014: Mirantis Inc.
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


openstack_data = {
    "auth_url": None,
    "username": None,
    "password": None,
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
    "insecure": False,
    "https_cacert": None,
    "cacert": None,
}


class GeneralCredential(object):
    _data = {}
    _creds_type = None

    def __init__(self, **kwargs):
        super(GeneralCredential, self).__init__()
        self._creds_type = kwargs.get("creds_type")
        self._data.update(kwargs)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return self._data[item]

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self._data[key] = value

    def to_dict(self):
        return self._data.copy()


class LegacyMetaCredential(object):

    def __new__(cls, *args, **kwargs):
        if "creds_type" not in kwargs:
            return super(LegacyMetaCredential, cls).__new__(
                OpenStackCredential, *args, **kwargs)
        return super(LegacyMetaCredential, cls).__new__(
            GeneralCredential, **kwargs)


class CredentialLegacyDict(object):
    _data = {}
    _creds_type = None

    def __init__(self, *args, **kwargs):
        super(CredentialLegacyDict, self).__init__()
        self._creds_type = kwargs.get("creds_type")
        if not self._creds_type or self._creds_type == "openstack":
            self._data.update(openstack_data)
            self._data.update(kwargs)
            if args and len(args) >= 3:
                self.auth_url = args[0]
                self.username = args[1]
                self.password = args[2]
            if "https_insecure" in kwargs:
                self.insecure = self.https_insecure
            if "https_cacert" in kwargs:
                self.cacert = self.https_cacert
            self.to_dict = self.openstack_creds_to_dict
        else:
            self._data.update(kwargs)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return self._data[item]

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        elif key == "to_dict":
            super(CredentialLegacyDict, self).__setattr__(key, value)
        else:
            self._data[key] = value

    def to_dict(self):
        return self._data.copy()

    def openstack_creds_to_dict(self, include_permission=False):
        dct = self._data.copy()
        if include_permission:
            dct["permission"] = self.permission
        return dct


class OpenStackCredential(object):

    def __init__(self, auth_url, username, password, tenant_name=None,
                 permission=consts.EndpointPermission.USER,
                 region_name=None, endpoint_type=consts.EndpointType.PUBLIC,
                 domain_name=None, endpoint=None,
                 user_domain_name="Default", admin_domain_name="Default",
                 project_domain_name="Default",
                 https_insecure=False, https_cacert=None):
        self.auth_url = auth_url
        self.username = username
        self.password = password
        self.tenant_name = tenant_name
        self.permission = permission
        self.region_name = region_name
        self.endpoint_type = endpoint_type
        self.domain_name = domain_name
        self.user_domain_name = user_domain_name
        self.admin_domain_name = admin_domain_name
        self.project_domain_name = project_domain_name
        self.endpoint = endpoint
        self.insecure = https_insecure
        self.cacert = https_cacert

    def to_dict(self, include_permission=False):
        dct = {"auth_url": self.auth_url, "username": self.username,
               "password": self.password, "tenant_name": self.tenant_name,
               "region_name": self.region_name,
               "endpoint_type": self.endpoint_type,
               "domain_name": self.domain_name,
               "endpoint": self.endpoint,
               "https_insecure": self.insecure,
               "https_cacert": self.cacert,
               "user_domain_name": self.user_domain_name,
               "admin_domain_name": self.admin_domain_name,
               "project_domain_name": self.project_domain_name}
        if include_permission:
            dct["permission"] = self.permission
        return dct


Credential = GeneralCredential

if __name__ == "__main__":
    Credential = GeneralCredential
    some_creds = Credential(
        "http://192.168.1.1:5000/v2.0/", "admin", "adminpass")
    print(some_creds)
    print(some_creds.to_dict())
    print(some_creds.to_dict(include_permission=True))
    some_creds = Credential(
        "http://192.168.1.1:5000/v2.0/", "admin", "adminpass", https_cacert="None")
    print(some_creds)
    print(some_creds.to_dict())
    print(some_creds.to_dict(include_permission=True))
    print(vars(some_creds))
    print(dir(some_creds))
    general_creds = GeneralCredential(
        auth_url="http://192.168.1.1:5000/v2.0/",
        username="admin",
        password="adminpass",
        https_cacert="None")
    print(general_creds)
    print(general_creds.to_dict())
