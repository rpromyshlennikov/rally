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

from rally.plugins.common import credentials
from tests.unit import test


fake_credentials_schema = {

    "type": "object",

    "properties": {
        "auth_url": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["auth_url", "username", "password"],

    "additionalProperties": False
}


@credentials.configure(name="fake_creds", schema=fake_credentials_schema)
class FakeCredentials(credentials.Credentials):
    pass


class CredentialsTestCase(test.TestCase):

    def test_to_dict(self):
        credential = credentials.Credentials.get("fake_creds")(
            dict(
                auth_url="foo_url",
                username="foo_user",
                password="foo_password",
            ))
        self.assertEqual(credential.to_dict(),
                         {"auth_url": "foo_url",
                          "username": "foo_user",
                          "password": "foo_password",
                          })

    def test_getattr(self):
        credential = credentials.Credentials.get("fake_creds")(
            dict(
                auth_url="foo_url",
                username="foo_user",
                password="foo_password"))
        self.assertEqual(credential.credentials,
                         {"auth_url": "foo_url",
                          "username": "foo_user",
                          "password": "foo_password",
                          })

    def test_getattr_raises(self):
        credential = credentials.Credentials.get("fake_creds")(
            dict(
                auth_url="foo_url",
                username="foo_user",
                password="foo_password",
            ))
        self.assertRaises(AttributeError, getattr, credential, "not-exist")
