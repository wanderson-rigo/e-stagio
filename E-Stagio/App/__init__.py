from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from config import Config

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

@app.template_filter('readable_status')
def readable_status(status_enum):
    translations = {
        'AGUARDANDO_APROVACAO': 'Aguardando aprovação',
        'APROVADO': 'Aprovado',
        'EM_ANDAMENTO': 'Em andamento',
        'FINALIZADO': 'Finalizado',
        'CANCELADO': 'Cancelado',
        'AGUARDANDO_AVALIACAO': 'Aguardando avaliação'
    }
    return translations.get(status_enum.name, 'Status desconhecido')

# Now it's safe to import models because 'db' has been defined
from app.models import User, Role

migrate = Migrate(app, db)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize Flask-Security with the custom register form
security = Security(app, user_datastore)

# Import routes after initializing models and extensions
from app import routes

#for rule in app.url_map.iter_rules():
#   print(rule)
