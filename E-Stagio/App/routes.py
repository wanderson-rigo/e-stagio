import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from app import app, db, mail
from flask_security.utils import hash_password
from app.models import User, Role, Professor
from flask_security import login_user, current_user, roles_required, login_required
from app.forms import ProfessorForm

@app.route('/send-test-email')
@roles_required('admin')
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

@app.route('/admin/cadastro-professor', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_professor():
    form = ProfessorForm()
    if form.validate_on_submit():
        # Criar o usuário primeiro
        hashed_password = hash_password(form.password.data)
        user = User(email=form.email.data, password=hashed_password, active=True)
        user.username = user.email
        user.confirmed_at = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()

        # Criar o professor e associá-lo ao usuário
        professor = Professor(nome=form.nome.data, cpf=form.cpf.data, email=form.email.data, user_id=user.id)
        db.session.add(professor)
        db.session.commit()

        flash('Professor cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('admin/cadastro_professor.html', form=form)
    
@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')  # For public/unlogged users
    elif 'admin' in current_user.roles:
        return render_template('admin/index_admin.html')  # For admin
    elif 'professor' in current_user.roles:
        return render_template('professor/index_professor.html')  # For teachers
    elif 'estudante' in current_user.roles:
        return render_template('estudante/index_estudante.html')  # For students
    elif 'empresa' in current_user.roles:
        return render_template('empresa/index_empresa.html')  # For companies
    elif 'supervisor' in current_user.roles:
        return render_template('supervisor/index_supervisor.html')  # For supervisors
    else:
        return render_template('index.html') 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    roles = Role.query.filter(Role.name != 'admin').all()
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
        role_id = request.form.get('options')
        role = Role.query.filter_by(id=role_id).first()
        if role:
            user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        # need to validate the email but not important by now
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