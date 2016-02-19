# Copyright (c) 2016 Mirantis Inc.
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


"""Add deployment type column

Revision ID: 1891b59eca2f
Revises: ca3626f62937
Create Date: 2016-02-04 19:02:36.566357

"""

# revision identifiers, used by Alembic.
revision = "1891b59eca2f"
down_revision = "ca3626f62937"
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    with op.batch_alter_table("deployments", schema=None) as batch_op:
        batch_op.add_column(sa.Column("type",
                                      sa.String(length=255),
                                      nullable=True))
    type_ = sa.table("deployments", sa.Column("type", sa.String))
    op.execute(
        type_.update().values({"type": op.inline_literal("openstack")})
    )

    with op.batch_alter_table("deployments", schema=None) as batch_op:
        batch_op.alter_column("type",
                              existing_type=sa.String(length=255),
                              existing_nullable=True,
                              nullable=False)


def downgrade():
    with op.batch_alter_table("deployments", schema=None) as batch_op:
        batch_op.drop_column("type")
