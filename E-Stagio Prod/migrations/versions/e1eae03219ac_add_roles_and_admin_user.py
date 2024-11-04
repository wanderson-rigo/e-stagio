from datetime import datetime
from flask_security.utils import hash_password

def upgrade():
    # Define a senha hash para o usuário admin
    hashed_password = hash_password('Admin123!')
    current_date = datetime.utcnow().isoformat()  # Data atual em UTC

    # Insere os papéis (roles) diretamente
    op.execute("INSERT INTO role (name, description) VALUES ('professor', 'Professor Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('empresa', 'Empresa Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('supervisor', 'Supervisor Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('aluno', 'Aluno Role')")
    op.execute("INSERT INTO role (name, description) VALUES ('admin', 'Admin Role')")

    # Insere o usuário admin com confirmed_at definido para hoje
    op.execute(f"""
        INSERT INTO "user" (username, email, password, active, fs_uniquifier, confirmed_at)
        VALUES (
            'admin',
            'admin@admin.com',
            '{hashed_password}',
            TRUE,
            'unique_identifier_for_admin',
            '{current_date}'
        )
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
