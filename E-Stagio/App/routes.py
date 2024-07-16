import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from app import app, db, mail
from flask_security.utils import hash_password
from app.models import User, Role, Professor, Empresa, Aluno, Supervisor
from flask_security import login_user, current_user, roles_required, login_required
from app.forms import ProfessorForm, EmpresaForm, AlunoForm, SupervisorForm

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
        try:
            hashed_password = hash_password(form.password.data)
            
            user = User(
                email=form.email.data,
                password=hashed_password,
                active=True,
                username=form.email.data,
                confirmed_at=datetime.datetime.now()
            )
            professor_role = Role.query.filter_by(name='professor').first()
            if professor_role:
                user.roles.append(professor_role)
            
            db.session.add(user)
            db.session.flush()

            professor = Professor(
                nome=form.nome.data,
                cpf=form.cpf.data,
                email=form.email.data,
                user_id=user.id,
                is_approved=True,
            )
            
            db.session.add(professor)
            db.session.commit()
            
            flash('Professor cadastrado com sucesso!', 'success')
            
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create professor. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_professor.html', form=form)
    
    return render_template('admin/cadastro_professor.html', form=form)

@app.route('/admin/cadastro-empresa', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_empresa():
    form = EmpresaForm()
    
    if form.validate_on_submit():
        try:
            hashed_password = hash_password(form.password.data)
            
            user = User(
                email=form.email.data,
                password=hashed_password,
                active=True,
                username=form.email.data,
                confirmed_at=datetime.datetime.now()
            )
            empresa_role = Role.query.filter_by(name='empresa').first()
            if empresa_role:
                user.roles.append(empresa_role)
            
            db.session.add(user)
            db.session.flush()

            empresa = Empresa(
                nome_empresa=form.nome.data,
                cnpj=form.cnpj.data,
                email_empresa=form.email.data,
                user_id=user.id, qsa=form.qsa.data,
                nome_responsavel=form.nome_responsavel.data,
                email_responsavel=form.email_responsavel.data,
                telefone_responsavel=form.telefone_responsavel.data,
                telefone_empresa=form.telefone.data,
                rg_responsavel=form.rg_responsavel.data,
                cpf_responsavel=form.cpf_responsavel.data,
                is_approved=True
            )
            
            db.session.add(empresa)
            db.session.commit()
            
            flash('Empresa cadastrada com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create professor. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_empresa.html', form=form)
    
    return render_template('admin/cadastro_empresa.html', form=form)

@app.route('/admin/cadastro-aluno', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_aluno():
    form = AlunoForm()
    
    if form.validate_on_submit():
        try:
            hashed_password = hash_password(form.password.data)
            email = form.email.data

            user = User(
                email=email,
                password=hashed_password,
                active=True,
                username=email,  # Ensure username is not None
                confirmed_at=datetime.datetime.now()
            )
            aluno_role = Role.query.filter_by(name='aluno').first()
            if aluno_role:
                user.roles.append(aluno_role)

            db.session.add(user)
            db.session.flush()

            aluno = Aluno(
                nome=form.nome.data,
                matricula=form.matricula.data,
                data_de_nascimento=form.dob.data,
                rg=form.rg.data,
                cpf=form.cpf.data,
                email=form.email.data,
                celular=form.celular.data,
                user_id=user.id,
                is_approved=True
            )

            db.session.add(aluno)
            db.session.commit()
            
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create aluno. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_aluno.html', form=form)

    return render_template('admin/cadastro_aluno.html', form=form)

@app.route('/admin/cadastro-supervisor', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_supervisor():
    form = SupervisorForm()
    form.empresaId.choices = [(empresa.id, empresa.nome_empresa) for empresa in Empresa.query.all()]
    
    if form.validate_on_submit():
        try:
            hashed_password = hash_password(form.password.data)
            
            user = User(
                email=form.email.data,
                password=hashed_password,
                active=True,
                username = form.email.data,
                confirmed_at = datetime.datetime.now()
            )
            
            supervisor_role = Role.query.filter_by(name='supervisor').first()
            if supervisor_role:
                user.roles.append(supervisor_role)
            
            db.session.add(user)
            db.session.flush()

            supervisor = Supervisor(
                nome=form.nome.data,
                cpf=form.cpf.data,
                email=form.email.data,
                user_id=user.id,
                formacao=form.formacao.data,
                empresa_id=form.empresaId.data,
                telefone=form.telefone.data
            )
            
            db.session.add(supervisor)
            db.session.commit()

            flash('Supervisor cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash(f'Failed to create Supervisor. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_supervisor.html', form=form)
        
    return render_template('admin/cadastro_supervisor.html', form=form)

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
        
        hashed_password = hash_password(request.form['password'])
        user = User(email=request.form['email'], active=True, password=hashed_password)
        user.username = user.email
        user.confirmed_at = datetime.datetime.now()
        
        role_id = request.form.get('options')
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
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if  user.password == request.form['password']:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg="Usuario ou Senha Incorretos"
        
        else:
            msg="Usuario ou Senha Incorretos"
        return render_template('signin.html', msg=msg)
        
    else:
        return render_template("signin.html", msg=msg)