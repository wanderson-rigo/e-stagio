from App import app, db
from App.models import User, Role

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}

if __name__ == '__main__':
    app.run(debug=True)