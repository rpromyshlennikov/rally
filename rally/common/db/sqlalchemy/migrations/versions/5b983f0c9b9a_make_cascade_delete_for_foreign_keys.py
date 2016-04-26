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

"""Make cascade delete for foreign key items

Revision ID: 5b983f0c9b9a
Revises: 3177d36ea270
Create Date: 2016-04-11 19:27:35.590097

"""

# revision identifiers, used by Alembic.
revision = "5b983f0c9b9a"
down_revision = "3177d36ea270"
branch_labels = None
depends_on = None


from alembic import op
from sqlalchemy.engine import reflection


naming_convention = {
    "fk":
    "%(table_name)s_ibfk_1",
}

tables = ("resources", "tasks", "task_results",
          "verifications", "verification_results")


def upgrade():
    insp = reflection.Inspector.from_engine(op.get_bind())
    for table in tables:
        fk = insp.get_foreign_keys(table)[0]
        fk_name = fk["name"] or "%s_ibfk_1" % table

        with op.batch_alter_table(
                table, naming_convention=naming_convention) as batch_op:
            batch_op.drop_constraint(fk_name, type_="foreignkey")
            batch_op.create_foreign_key(
                fk_name, fk["referred_table"],
                fk["constrained_columns"], fk["referred_columns"],
                ondelete="CASCADE"
            )


def downgrade():
    insp = reflection.Inspector.from_engine(op.get_bind())
    for table in tables:
        fk = insp.get_foreign_keys(table)[0]
        fk_name = fk["name"] or "%s_ibfk_1" % table

        with op.batch_alter_table(
                table, naming_convention=naming_convention) as batch_op:
            batch_op.drop_constraint(fk_name, type_="foreignkey")
            batch_op.create_foreign_key(
                fk_name, fk["referred_table"],
                fk["constrained_columns"], fk["referred_columns"]
            )
