class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Admin123@localhost/estagio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'key' # TODO change to a safer one
    MAIL_SERVER = 'smtp-relay.brevo.com'  # O servidor SMTP do seu provedor de e-mail
    MAIL_PORT = 587  # Geralmente 587 para TLS, 465 para SSL
    MAIL_USE_TLS = True  # Ativar TLS (True ou False)
    MAIL_USE_SSL = False  # Ativar SSL (True ou False), não use com TLS
    MAIL_USERNAME = 'e-stagiovideira@hotmail.com'  # Seu endereço de e-mail
    MAIL_PASSWORD = 'm6R35S87yOJULpKd'  # Sua senha de e-mail
    MAIL_DEFAULT_SENDER = 'e-stagiovideira@hotmail.com'  # O endereço de e-mail padrão para enviar e-mails
    SECURITY_REGISTERABLE= True # Se você deseja permitir que os usuários se registrem.
    SECURITY_CONFIRMABLE= True # Se você deseja que os usuários confirmem seus endereços de e-mail.
    SECURITY_RECOVERABLE= True # Se você deseja permitir a recuperação de senha.
    SECURITY_TRACKABLE= True # Se você deseja rastrear informações de login do usuário.
    SECURITY_PASSWORD_SALT = 'W4#s$8Fp!2Yq^7@z'
