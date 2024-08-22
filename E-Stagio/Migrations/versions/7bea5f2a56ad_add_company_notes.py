"""Add company notes

Revision ID: 7bea5f2a56ad
Revises: 215e05e1806e
Create Date: 2024-08-22 10:24:29.961631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bea5f2a56ad'
down_revision = '215e05e1806e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('empresa_nota_interesse', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_iniciativa', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_cooperacao', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_assiduidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_pontualidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_disciplina', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_sociabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_adaptabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_responsabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_nota_etica', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('empresa_atividades', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('emprsa_comentarios', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('empresa_media_notas', sa.Float(), nullable=True))
        batch_op.create_foreign_key(None, 'alunos', ['aluno_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('empresa_media_notas')
        batch_op.drop_column('emprsa_comentarios')
        batch_op.drop_column('empresa_atividades')
        batch_op.drop_column('empresa_nota_etica')
        batch_op.drop_column('empresa_nota_responsabilidade')
        batch_op.drop_column('empresa_nota_adaptabilidade')
        batch_op.drop_column('empresa_nota_sociabilidade')
        batch_op.drop_column('empresa_nota_disciplina')
        batch_op.drop_column('empresa_nota_pontualidade')
        batch_op.drop_column('empresa_nota_assiduidade')
        batch_op.drop_column('empresa_nota_cooperacao')
        batch_op.drop_column('empresa_nota_iniciativa')
        batch_op.drop_column('empresa_nota_interesse')

    # ### end Alembic commands ###
