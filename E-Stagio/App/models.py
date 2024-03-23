import uuid
from App import db
from flask_security import UserMixin, RoleMixin

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    roles = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username}>'
