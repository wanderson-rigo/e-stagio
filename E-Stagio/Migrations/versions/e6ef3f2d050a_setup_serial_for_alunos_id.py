"""Setup SERIAL for alunos id

Revision ID: e6ef3f2d050a
Revises: 348a4c13109f
Create Date: 2024-07-13 19:24:27.655633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6ef3f2d050a'
down_revision = '348a4c13109f'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('DROP TABLE IF EXISTS alunos CASCADE;') # Be cautious with this in production; ensure data is backed up if necessary.
    op.create_table('alunos',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('matricula', sa.String(length=20), unique=True, nullable=False),
        sa.Column('data_de_nascimento', sa.Date(), nullable=False),
        sa.Column('rg', sa.String(length=20), nullable=False),
        sa.Column('cpf', sa.String(length=14), unique=True, nullable=False),
        sa.Column('email', sa.String(length=100), unique=True, nullable=False),
        sa.Column('celular', sa.String(length=15), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('is_approved', sa.Boolean(), nullable=False)
    )


def downgrade():
    op.drop_table('alunos')
