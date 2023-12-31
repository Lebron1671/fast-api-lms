"""Add set null for Course

Revision ID: c07a1ead0e62
Revises: 1e2990baf0bc
Create Date: 2023-08-08 16:44:14.600203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c07a1ead0e62'
down_revision: Union[str, None] = '1e2990baf0bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('courses_teacher_id_fkey', 'courses', type_='foreignkey')
    op.create_foreign_key(None, 'courses', 'users', ['teacher_id'], ['id'], onupdate='set null')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'courses', type_='foreignkey')
    op.create_foreign_key('courses_teacher_id_fkey', 'courses', 'users', ['teacher_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###
