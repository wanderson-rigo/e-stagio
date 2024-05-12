from app.models import Role, User
from app import app, db, user_datastore
from flask_security.utils import hash_password

# Função para adicionar roles
def add_roles():
    roles = ['professor', 'empresa', 'supervisor', 'aluno', 'admin']
    for role_name in roles:
        if not user_datastore.find_role(role_name):
            user_datastore.create_role(name=role_name)
    db.session.commit()

def add_admin():
    if not User.query.filter_by(email='admin@example.com').first():
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password=hash_password('Admin123!'),  # Senha hasheada
                role_id=admin_role.id  # Associa a role 'admin' ao usuário
            )
            
            db.session.add(admin_user)
            db.session.commit()
        else:
            print("Role 'admin' not found. Please make sure to add roles first.")

if __name__ == '__main__':
    with app.app_context():
        add_roles()
        add_admin()
