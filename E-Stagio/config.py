class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Admin123@localhost/estagio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'key' # TODO change to a safer one