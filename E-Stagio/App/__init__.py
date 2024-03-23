from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore

# Inicialize o Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicialize o SQLAlchemy
db = SQLAlchemy(app)

# Agora é seguro importar os modelos porque 'db' já foi definido
from App.models import User, Role

migrate = Migrate(app, db)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Importe as rotas após a inicialização dos modelos e extensões
from App import routes
