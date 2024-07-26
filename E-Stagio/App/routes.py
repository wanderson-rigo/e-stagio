import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request
from app import app, db, mail
from flask_security.utils import hash_password
from app.models import User, Role, Professor, Empresa, Aluno, Supervisor, Estagio
from flask_security import login_user, current_user, roles_required, login_required
from app.forms import ProfessorForm, EmpresaForm, AlunoForm, SupervisorForm, EstagioForm, ProfessorFormEdit, SupervisorEditForm, AlunoEditForm, EmpresaEditForm

@app.route('/send-test-email')
@roles_required('admin')
def send_test_email():
    try:
        msg = Message("Test Email",
                      recipients=["brunopergher_1@hotmail.com"],  # Substitua pelo endereço de e-mail do destinatário
                      body="This is a test email sent from Flask-Mail.")
        
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

@app.route('/admin/cadastro-estagio', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_estagio():
    form = EstagioForm()
    form.aluno_id.choices = [(a.id, a.nome) for a in Aluno.query.all()]
    form.professor_id.choices = [(p.id, p.nome) for p in Professor.query.all()]
    form.supervisor_id.choices = [(s.id, s.nome) for s in Supervisor.query.all()]
    form.empresa_id.choices = [(e.id, e.nome_empresa) for e in Empresa.query.all()]

    if form.validate_on_submit():
        try:
            estagio = Estagio(
                aluno_id=form.aluno_id.data,
                professor_id=form.professor_id.data,
                supervisor_id=form.supervisor_id.data,
                empresa_id=form.empresa_id.data,
                modalidade=form.modalidade.data,
                carga_horaria=form.carga_horaria.data,
                atividades=form.atividades.data,
                setor=form.setor.data,
                remuneracao=form.remuneracao.data,
                valor_remuneracao=form.valor_remuneracao.data if form.remuneracao.data else None,
                horario_estagio=form.horario_estagio.data,
                data_inicio=form.data_inicio.data,
                data_conclusao=form.data_conclusao.data,
                is_approved=True
            )
            
            db.session.add(estagio)
            db.session.commit()
            
            flash('Estágio cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create estágio. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_estagio.html', form=form)

    return render_template('admin/cadastro_estagio.html', form=form)

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

@app.route('/admin/professores')
@roles_required('admin')
def lista_professores():
    professores = Professor.query.all()
    return render_template('admin/listagem_professores.html', professores=professores)

@app.route('/admin/supervisores', methods=['GET', 'POST'])
@roles_required('admin')
def lista_supervisores():
    supervisores = Supervisor.query.join(Empresa, Supervisor.empresa_id == Empresa.id).all()
    return render_template('admin/listagem_supervisores.html', supervisores=supervisores)

@app.route('/admin/alunos')
@roles_required('admin')
def lista_alunos():
    alunos = Aluno.query.all()
    return render_template('admin/listagem_alunos.html', alunos=alunos)

@app.route('/admin/empresas')
@roles_required('admin')
def lista_empresas():
    empresas = Empresa.query.all()
    return render_template('admin/listagem_empresas.html', empresas=empresas)

@app.route('/admin/estagios', methods=['GET'])
@roles_required('admin')
def lista_estagios():
    estagios = Estagio.query.all()
    return render_template('admin/listagem_estagios.html', estagios=estagios)

@app.route('/admin/editar-empresa/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    form = EmpresaEditForm(obj=empresa)

    if form.validate_on_submit():
        try:
            empresa.nome_empresa = form.nome_empresa.data
            empresa.email_empresa = form.email_empresa.data
            empresa.telefone_empresa = form.telefone_empresa.data
            empresa.cnpj = form.cnpj.data
            empresa.qsa = form.qsa.data
            empresa.nome_responsavel = form.nome_responsavel.data
            empresa.email_responsavel = form.email_responsavel.data
            empresa.telefone_responsavel = form.telefone_responsavel.data
            empresa.rg_responsavel = form.rg_responsavel.data
            empresa.cpf_responsavel = form.cpf_responsavel.data
            
            db.session.commit()
            flash('Empresa atualizada com sucesso!', 'success')
            return redirect(url_for('lista_empresas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar empresa: {e}', 'error')

    return render_template('admin/editar_empresa.html', form=form)

@app.route('/admin/editar-aluno/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    form = AlunoEditForm(obj=aluno)

    if form.validate_on_submit():
        aluno.nome = form.nome.data
        aluno.email = form.email.data
        aluno.cpf = form.cpf.data
        aluno.rg = form.rg.data
        aluno.data_de_nascimento = form.dob.data
        aluno.celular = form.celular.data
        aluno.matricula = form.matricula.data

        try:
            db.session.commit()
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('lista_alunos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar aluno. {str(e)}', 'error')

    return render_template('admin/editar_aluno.html', form=form)

@app.route('/admin/editar-supervisor/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_supervisor(id):
    supervisor = Supervisor.query.get_or_404(id)
    form = SupervisorEditForm(obj=supervisor)

    if form.validate_on_submit():
        try:
            supervisor.nome = form.nome.data
            supervisor.email = form.email.data
            supervisor.telefone = form.telefone.data
            supervisor.cpf = form.cpf.data
            supervisor.formacao = form.formacao.data
            supervisor.empresa_id = form.empresaId.data

            db.session.commit()
            flash('Supervisor atualizado com sucesso!', 'success')
            return redirect(url_for('lista_supervisores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar supervisor. {str(e)}', 'error')

    return render_template('admin/editar_supervisor.html', form=form)

@app.route('/admin/editar-professor/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_professor(id):
    professor = Professor.query.get_or_404(id)
    form = ProfessorFormEdit(obj=professor)
    if form.validate_on_submit():
        print("aqui")
        try:
            print(form.data)
            professor.nome = form.nome.data
            professor.email = form.email.data
            professor.cpf = form.cpf.data
            db.session.add(professor)
            db.session.commit()
            flash('Professor atualizado com sucesso!', 'success')
            return redirect(url_for('lista_professores'))
        except Exception as e:
            print(e)
            print('Error:', str(e))
            db.session.rollback()
            flash(f'Erro ao atualizar professor. {str(e)}', 'danger')

    return render_template('admin/editar_professor.html', form=form, professor=professor)

@app.route('/admin/editar-estagio/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_estagio(id):
    estagio = Estagio.query.get_or_404(id)
    form = EstagioForm(obj=estagio)

    if form.validate_on_submit():
        try:
            estagio.aluno_id = form.aluno_id.data
            estagio.professor_id = form.professor_id.data
            estagio.supervisor_id = form.supervisor_id.data
            estagio.empresa_id = form.empresa_id.data
            estagio.modalidade = form.modalidade.data
            estagio.carga_horaria = form.carga_horaria.data
            estagio.atividades = form.atividades.data
            estagio.setor = form.setor.data
            estagio.remuneracao = form.remuneracao.data
            estagio.valor_remuneracao = form.valor_remuneracao.data
            estagio.horario_estagio = form.horario_estagio.data
            estagio.data_inicio = form.data_inicio.data
            estagio.data_conclusao = form.data_conclusao.data
            estagio.is_approved = form.is_approved.data

            db.session.commit()
            flash('Estágio atualizado com sucesso!', 'success')
            return redirect(url_for('lista_estagios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar estágio: {e}', 'error')

    return render_template('admin/editar_estagio.html', form=form, estagio=estagio)

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