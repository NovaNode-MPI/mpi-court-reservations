"""add reservation status lifecycle constraint

Revision ID: 6f57ccdfdcc1
Revises: d319da9124f8
Create Date: 2026-03-22 18:32:05.612456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f57ccdfdcc1'
down_revision: Union[str, None] = 'd319da9124f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
