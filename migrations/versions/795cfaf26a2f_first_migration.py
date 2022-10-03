"""First migration

Revision ID: 795cfaf26a2f
Revises:
Create Date: 2022-10-03 21:09:32.402312

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "795cfaf26a2f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "atms",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("provider", sa.String(), nullable=True),
        sa.Column(
            "geography",
            geoalchemy2.types.Geography(
                geometry_type="POINT", srid=4326, from_text="ST_GeogFromText", name="geography"
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # op.create_index('idx_atms_geography', 'atms', ['geography'],
    # unique=False, postgresql_using='gist')


def downgrade() -> None:
    # op.drop_index('idx_atms_geography', table_name='atms', postgresql_using='gist')
    op.drop_table("atms")
