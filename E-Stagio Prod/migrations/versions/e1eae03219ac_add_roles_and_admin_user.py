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
    app = current_app._get_current_object()
    with app.app_context():
        from app import user_datastore, db
        
        roles = ['professor', 'empresa', 'supervisor', 'aluno', 'admin']
        for role_name in roles:
            if not user_datastore.find_role(role_name):
                user_datastore.create_role(name=role_name)
        db.session.commit()

        if not user_datastore.find_user(email='admin@admin.com'):
            admin_role = user_datastore.find_or_create_role('admin')

            admin_user = user_datastore.create_user(
                username='admin',
                email='admin@admin.com',
                password=hash_password('Admin123!'),
                active=True
            )

            user_datastore.add_role_to_user(admin_user, admin_role)
            db.session.commit()

def downgrade():
    app = current_app._get_current_object()
    with app.app_context():
        from app import user_datastore, db

        admin_user = user_datastore.find_user(email='admin@admin.com')
        if admin_user:
            db.session.delete(admin_user)
        
        for role_name in ['professor', 'empresa', 'supervisor', 'aluno', 'admin']:
            role = user_datastore.find_role(role_name)
            if role:
                db.session.delete(role)
        
        db.session.commit()
