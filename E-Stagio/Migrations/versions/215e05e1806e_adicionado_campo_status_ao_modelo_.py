"""Adicionado campo status ao modelo Estagio

Revision ID: 215e05e1806e
Revises: e6ef3f2d050a
Create Date: 2024-07-27 01:01:18.564319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215e05e1806e'
down_revision = 'e6ef3f2d050a'
branch_labels = None
depends_on = None

def upgrade():
    # Cria o enum no PostgreSQL
    status_type = sa.Enum('AGUARDANDO_APROVACAO', 'APROVADO', 'EM_ANDAMENTO', 'FINALIZADO', 'CANCELADO', 'AGUARDANDO_AVALIACAO', name='statusestagio')
    status_type.create(op.get_bind(), checkfirst=True)

    # Comandos autogerados pelo Alembic ajustados
    with op.batch_alter_table('alunos', schema=None) as batch_op:
        batch_op.alter_column('is_approved',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', status_type, nullable=False, server_default='AGUARDANDO_APROVACAO'))

def downgrade():
    # Comandos autogerados pelo Alembic ajustados
    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.drop_column('status')

    status_type = sa.Enum('AGUARDANDO_APROVACAO', 'APROVADO', 'EM_ANDAMENTO', 'FINALIZADO', 'CANCELADO', 'AGUARDANDO_AVALIACAO', name='statusestagio')
    status_type.drop(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('alunos', schema=None) as batch_op:
        batch_op.alter_column('is_approved',
               existing_type=sa.BOOLEAN(),
               nullable=False)
