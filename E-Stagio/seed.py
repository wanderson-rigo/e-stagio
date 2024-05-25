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
    # Check if the admin user already exists
    if not user_datastore.find_user(email='admin@admin.com'):
        # Find or create the 'admin' role
        admin_role = user_datastore.find_or_create_role('admin')

        # Create the admin user with hashed password
        admin_user = user_datastore.create_user(
            username='admin2',
            email='admin@admin.com',
            password=hash_password('Admin123!')
        )

        # Add admin role to the admin user
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    with app.app_context():
        add_roles()
        add_admin()
