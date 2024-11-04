"""Add roles and admin user

Revision ID: e1eae03219ac
Revises: c594222efc6c
Create Date: 2024-11-03 23:38:58.238535

"""
from alembic import op
from flask import current_app
from flask_security.utils import hash_password

# revision identifiers, used by Alembic.
revision = 'e1eae03219ac'
down_revision = 'c594222efc6c'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("INSERT INTO role (name, description) VALUES ('professor', 'Professor Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('empresa', 'Empresa Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('supervisor', 'Supervisor Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('aluno', 'Aluno Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('admin', 'Admin Role')")
    
    # Inserção do usuário admin diretamente
    hashed_password = hash_password('Admin123!')
    confirmed_date = '2024-11-04 00:00:00'
    op.execute(f"""
        INSERT INTO "user" (username, email, password, active, fs_uniquifier, confirmed_at)
        VALUES ('admin', 'admin@admin.com', '{hashed_password}', TRUE, 'unique_identifier_for_admin', '{confirmed_date}')
    """)
    
    # Associando o papel de admin ao usuário admin criado
    op.execute("""
        INSERT INTO roles_users (user_id, role_id)
        VALUES (
            (SELECT id FROM "user" WHERE email = 'admin@admin.com'),
            (SELECT id FROM role WHERE name = 'admin')
        )
    """)

def downgrade():
    op.execute("DELETE FROM roles_users WHERE user_id = (SELECT id FROM \"user\" WHERE email = 'admin@admin.com')")
    op.execute("DELETE FROM \"user\" WHERE email = 'admin@admin.com'")
    op.execute("DELETE FROM role WHERE name IN ('professor', 'empresa', 'supervisor', 'aluno', 'admin')")
