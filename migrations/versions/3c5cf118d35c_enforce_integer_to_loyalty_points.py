"""enforce integer to loyalty points

Revision ID: 3c5cf118d35c
Revises: cc69d3561c69
Create Date: 2023-09-08 00:23:45.876366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c5cf118d35c'
down_revision: Union[str, None] = 'cc69d3561c69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
