import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from app import app, db, mail
from flask_security.utils import hash_password
from app.models import User, Role
from flask_security import login_user

@app.route('/send-test-email')
def send_test_email():
    try:
        # Cria a mensagem
        msg = Message("Test Email",
                      recipients=["brunopergher_1@hotmail.com"],  # Substitua pelo endereço de e-mail do destinatário
                      body="This is a test email sent from Flask-Mail.")
        
        # Envia a mensagem
        mail.send(msg)
        
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"
    
@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    roles = Role.query.all()  # Query all roles to display in the form
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            msg = "User already exists"
            return render_template('signup.html', msg=msg, roles=roles)
        
        # If user doesn't exist, create a new user
        hashed_password = hash_password(request.form['password'])
        user = User(email=request.form['email'], active=True, password=hashed_password)
        user.username = user.email
        user.confirmed_at = datetime.datetime.now()
        
        # Store the role
        role_id = request.form.get('options')  # Get the role ID from the form
        role = Role.query.filter_by(id=role_id).first()
        if role:
            user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Por favor, confira seu e-mail para verificar sua conta.', 'success')
        
        return redirect(url_for('index'))
    else:
        return render_template("signup.html", msg=msg, roles=roles)
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if  user.password == request.form['password']:
                # if password matches, login the user
                login_user(user)
                return redirect(url_for('index'))
            # if password doesn't match
            else:
                msg="Wrong password"
        
        # if user does not exist
        else:
            msg="User doesn't exist"
        return render_template('signin.html', msg=msg)
        
    else:
        return render_template("signin.html", msg=msg)