from App import app, db
from App.models import Role, User
from werkzeug.security import generate_password_hash

def add_roles():
    roles = ['professores', 'empresas', 'supervisores', 'alunos', 'admin']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()

def add_admin():
    if not User.query.filter_by(username='admin').first():
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Admin role not found, please add roles first.")
            return
        
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('Admin123'),
            email='admin@admin.com',
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_roles()
        add_admin()
