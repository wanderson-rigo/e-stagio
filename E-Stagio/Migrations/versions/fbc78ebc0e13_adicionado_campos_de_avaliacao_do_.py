"""Adicionado campos de avaliacao do supervisor no Estagio

Revision ID: fbc78ebc0e13
Revises: 7bea5f2a56ad
Create Date: 2024-09-01 22:43:45.323511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbc78ebc0e13'
down_revision = '7bea5f2a56ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('supervisor_nota_interesse', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_iniciativa', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_cooperacao', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_assiduidade_e_pontuabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_criatividade_e_engenhosidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_disciplina', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_sociabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_adaptabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_responsabilidade', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_evolucao_tecnica', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_nota_etica', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_atividades', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_comentarios', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('supervisor_media_notas', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('estagios', schema=None) as batch_op:
        batch_op.drop_column('supervisor_media_notas')
        batch_op.drop_column('supervisor_comentarios')
        batch_op.drop_column('supervisor_atividades')
        batch_op.drop_column('supervisor_nota_etica')
        batch_op.drop_column('supervisor_evolucao_tecnica')
        batch_op.drop_column('supervisor_nota_responsabilidade')
        batch_op.drop_column('supervisor_nota_adaptabilidade')
        batch_op.drop_column('supervisor_nota_sociabilidade')
        batch_op.drop_column('supervisor_nota_disciplina')
        batch_op.drop_column('supervisor_nota_criatividade_e_engenhosidade')
        batch_op.drop_column('supervisor_nota_assiduidade_e_pontuabilidade')
        batch_op.drop_column('supervisor_nota_cooperacao')
        batch_op.drop_column('supervisor_nota_iniciativa')
        batch_op.drop_column('supervisor_nota_interesse')

    # ### end Alembic commands ###