import datetime
from datetime import datetime
from flask_mail import Message
from flask import render_template, redirect, url_for, flash, request, send_file, jsonify
from app import app, db, mail
from flask_security.utils import hash_password
from app.models import User, Role, Professor, Empresa, Aluno, Supervisor, Estagio, StatusEstagio, AtividadesEstagio
from flask_security import login_user, current_user, roles_required, login_required
from app.forms import *
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_
import fitz
import os
from io import BytesIO
from collections import defaultdict
import locale
import zipfile

# Inicio Area Geral

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

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')  # For public/unlogged users
    elif 'admin' in current_user.roles:
        return render_template('admin/index_admin.html')  # For admin
    elif 'professor' in current_user.roles:
        return redirect(url_for('index_professor'))
    elif 'aluno' in current_user.roles:
        return redirect(url_for('index_aluno'))
    elif 'empresa' in current_user.roles:
        return redirect(url_for('index_empresa'))
    elif 'supervisor' in current_user.roles:
        return redirect(url_for('index_supervisor'))
    else:
        return render_template('index.html') 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    roles = Role.query.filter(Role.name != 'admin').all()
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            msg = "Email já esta em uso"
            return render_template('signup.html', msg=msg, roles=roles)
        
        hashed_password = hash_password(request.form['password'])
        user = User(email=request.form['email'], active=False, password=hashed_password)
        user.username = user.email
        user.confirmed_at = datetime.datetime.now()
        
        role_id = request.form.get('options')
        role = Role.query.filter_by(id=role_id).first()
        if role:
            user.roles.append(role)
        
        db.session.add(user)
        db.session.commit()
        flash('Por favor, aguarde sua conta ser aprovada pelo setor de estágios para começar usar sua conta.', 'success')
        
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

# Fim Area Geral

# Inicio Area de Cadastros Admin

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
    form.empresaId.choices = [
        (e.id, e.nome_empresa) for e in Empresa.query.join(Empresa.user).filter(Empresa.is_approved == True, User.active == True).all()
    ]
    
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
                telefone=form.telefone.data,
                is_approved=True 
            )
            
            db.session.add(supervisor)
            db.session.commit()

            flash('Supervisor cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create Supervisor. Error: {str(e)}', 'error')
            return render_template('admin/cadastro_supervisor.html', form=form)
        
    return render_template('admin/cadastro_supervisor.html', form=form)

@app.route('/admin/cadastro-estagio', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_estagio():
    form = EstagioForm()
    
    # Preencher as opções de alunos, professores e empresas
    form.aluno_id.choices = [
        (a.id, a.nome) for a in Aluno.query.join(Aluno.user).filter(Aluno.is_approved == True, User.active == True).all()
    ]

    form.professor_id.choices = [
        (p.id, p.nome) for p in Professor.query.join(Professor.user).filter(Professor.is_approved == True, User.active == True).all()
    ]

    form.empresa_id.choices = [
        (e.id, e.nome_empresa) for e in Empresa.query.join(Empresa.user).filter(Empresa.is_approved == True, User.active == True).all()
    ]

    # Preencher as opções de supervisores dinamicamente com base na empresa selecionada
    empresa_id = request.form.get('empresa_id')
    if empresa_id:
        form.supervisor_id.choices = [
            (s.id, s.nome) for s in Supervisor.query.filter(Supervisor.empresa_id == int(empresa_id), Supervisor.is_approved == True).all()
        ]
    else:
        form.supervisor_id.choices = []

    form.status.choices = [(choice.name, choice.value.replace('_', ' ').title()) for choice in StatusEstagio]

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
                is_approved=True,
                status=form.status.data
            )

            db.session.add(estagio)
            db.session.commit()

            flash('Estágio cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to create estágio. Error: {str(e)}', 'error')
    else:
        flash(f'Formulário inválido: {form.errors}', 'error')

    return render_template('admin/cadastro_estagio.html', form=form)

@app.route('/get_supervisores/<int:empresa_id>', methods=['GET'])
@roles_required('admin')
def get_supervisores(empresa_id):
    supervisores = Supervisor.query.filter_by(empresa_id=empresa_id, is_approved=True).all()
    supervisores_data = [{'id': s.id, 'nome': s.nome} for s in supervisores]

    return jsonify({'supervisores': supervisores_data})

@app.route('/admin/cadastro-admin', methods=['GET', 'POST'])
@roles_required('admin')
def cadastro_admin():
    form = AdminForm()

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
            
            admin_role = Role.query.filter_by(name='admin').first()
            if admin_role:
                user.roles.append(admin_role)
            
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            
            flash('Novo Admin cadastrado com sucesso!', 'success')
            
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Falha para criar um admim. Erro: {str(e)}', 'error')
            return render_template('admin/cadastro_admin.html', form=form)
    
    return render_template('admin/cadastro_admin.html', form=form)

# Fim Area de Cadastros Admin

# Inicio Area de Listagem Admin

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

@app.route('/admin/admins', methods=['GET'])
@roles_required('admin')
def lista_admin():
    admins = User.query.join(User.roles).filter(Role.name == 'admin').options(joinedload(User.roles)).all()
    return render_template('admin/listagem_admin.html', admins=admins)

@app.route('/admin/listar-usuarios-inativos', methods=['GET'])
@roles_required('admin')
def listar_usuarios_inativos():
    usuarios_inativos = User.query.filter_by(active=False).all()
    return render_template('admin/listagem_usuarios_inativos.html', usuarios=usuarios_inativos)

@app.route('/admin/ativar-usuario/<int:user_id>', methods=['GET', 'POST'])
@roles_required('admin')
def ativar_usuario(user_id):
    usuario = User.query.get_or_404(user_id)
    if not usuario.active:
        try:
            usuario.active = True
            usuario.confirmed_at = datetime.datetime.now()
            db.session.commit()
            flash('Usuário ativado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao ativar usuário: {str(e)}', 'error')
    else:
        flash('Usuário já está ativo.', 'info')
    return redirect(url_for('listar_usuarios_inativos'))

# Fim Area de Listagem Admin

# Inicio Area de Edição Admin
@app.route('/admin/editar-empresa/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    user = empresa.user
    form = EmpresaEditForm(obj=empresa)
    
    if request.method == 'GET':
        form.ativo.data = user.active 

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
            user.active = form.ativo.data
            
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
    user = aluno.user
    form = AlunoEditForm(obj=aluno)
    
    if request.method == 'GET':
        form.ativo.data = user.active
        form.dob.data = aluno.data_de_nascimento

    if form.validate_on_submit():
        aluno.nome = form.nome.data
        aluno.email = form.email.data
        aluno.cpf = form.cpf.data
        aluno.rg = form.rg.data
        aluno.data_de_nascimento = form.dob.data
        aluno.celular = form.celular.data
        aluno.matricula = form.matricula.data
        user.active = form.ativo.data

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
    user = supervisor.user
    form = SupervisorEditForm(obj=supervisor)
    
    empresas_choices = Empresa.query.join(User).filter(
        or_(
            Empresa.id == supervisor.empresa_id, 
            and_(Empresa.is_approved == True, User.active == True)
        )
    ).all()
    
    form.empresaId.choices = [(empresa.id, empresa.nome_empresa) for empresa in empresas_choices]
    
    if request.method == 'GET':
        form.ativo.data = user.active
        form.empresaId.data = supervisor.empresa_id

    if form.validate_on_submit():
        try:
            supervisor.nome = form.nome.data
            supervisor.email = form.email.data
            supervisor.telefone = form.telefone.data
            supervisor.cpf = form.cpf.data
            supervisor.formacao = form.formacao.data
            supervisor.empresa_id = form.empresaId.data
            user.active = form.ativo.data

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
    user = professor.user
    form = ProfessorFormEdit(obj=professor)
    
    if request.method == 'GET':
        form.ativo.data = user.active 
        
    if form.validate_on_submit():
        try:
            professor.nome = form.nome.data
            professor.email = form.email.data
            professor.cpf = form.cpf.data
            user.active = form.ativo.data 
            
            db.session.add(professor)
            db.session.commit()
            flash('Professor atualizado com sucesso!', 'success')
            return redirect(url_for('lista_professores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar professor. {str(e)}', 'danger')

    return render_template('admin/editar_professor.html', form=form, professor=professor)

@app.route('/admin/editar-admin/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_admin(id):
    admin = User.query.get_or_404(id)
    form = AdminForm(obj=admin)
    
    if request.method == 'GET':
        form.ativo.data = admin.active 
        
    if form.validate_on_submit():
        try:
            admin.email = form.email.data
            admin.username = form.email.data
            admin.active = form.ativo.data 
            
            db.session.commit()
            flash('Admin atualizado com sucesso!', 'success')
            return redirect(url_for('lista_admin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar Admin. {str(e)}', 'danger')

    return render_template('admin/editar_admin.html', form=form, admin=admin)

@app.route('/admin/editar-estagio/<int:id>', methods=['GET', 'POST'])
@roles_required('admin')
def editar_estagio(id):
    estagio = Estagio.query.get_or_404(id)
    form = EstagioForm(obj=estagio)

    # Preencher as opções de alunos e professores
    form.aluno_id.choices = [
        (a.id, a.nome) for a in Aluno.query.join(Aluno.user).filter(
            or_(
                Aluno.id == estagio.aluno_id,
                and_(Aluno.is_approved == True, User.active == True)
            )
        ).all()
    ]

    form.professor_id.choices = [
        (p.id, p.nome) for p in Professor.query.join(Professor.user).filter(
            or_(
                Professor.id == estagio.professor_id,
                and_(Professor.is_approved == True, User.active == True)
            )
        ).all()
    ]

    form.empresa_id.choices = [
        (e.id, e.nome_empresa) for e in Empresa.query.join(Empresa.user).filter(
            or_(
                Empresa.id == estagio.empresa_id,
                and_(Empresa.is_approved == True, User.active == True)
            )
        ).all()
    ]

    # Preencher as opções de supervisores com base na empresa atual
    empresa_id = form.empresa_id.data
    if empresa_id:
        form.supervisor_id.choices = [
            (s.id, s.nome) for s in Supervisor.query.join(Supervisor.user).filter(
                or_(
                    Supervisor.id == estagio.supervisor_id,
                    and_(
                        Supervisor.empresa_id == empresa_id,
                        Supervisor.is_approved == True,
                        User.active == True
                    )
                )
            ).all()
        ]
    else:
        form.supervisor_id.choices = []

    form.status.choices = [(choice.name, choice.value.replace('_', ' ').title()) for choice in StatusEstagio]

    # Definir os valores iniciais do formulário (GET)
    if request.method == 'GET':
        form.aluno_id.data = estagio.aluno_id
        form.professor_id.data = estagio.professor_id
        form.supervisor_id.data = estagio.supervisor_id
        form.empresa_id.data = estagio.empresa_id
        form.status.data = estagio.status.name

    # Atualizar o estágio ao submeter o formulário (POST)
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
            estagio.status = StatusEstagio[form.status.data]

            db.session.merge(estagio)
            db.session.commit()
            flash('Estágio atualizado com sucesso!', 'success')
            return redirect(url_for('lista_estagios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar estágio: {e}', 'error')
    else:
        flash(f'Formulário inválido: {form.errors}', 'error')

    return render_template('admin/editar_estagio.html', form=form, estagio=estagio)
# Fim Area de Edição Admin

# Inicio Area Empresa

@app.route('/home-empresa', methods=['GET'])
@roles_required('empresa')
def index_empresa():
    estagios = Estagio.query.join(Empresa, Estagio.empresa_id == Empresa.id) \
                        .filter(Empresa.user_id == current_user.id).all()
    
    return render_template('empresa/index_empresa.html', estagios=estagios)

@app.route('/empresa/avaliacao/<int:estagio_id>', methods=['GET', 'POST'])
@roles_required('empresa')
def avaliacao_empresa(estagio_id):
    # Busca o estágio específico vinculado à empresa atual
    estagio = Estagio.query.join(Empresa).filter(
        Estagio.id == estagio_id,
        Empresa.user_id == current_user.id
    ).first_or_404()

    # Instancia o formulário passando o estagio como objeto, para preencher os campos se já houverem notas
    form = EmpresaAvaliacaoForm(obj=estagio)

    if form.validate_on_submit():
        try:
            # Atualiza as notas e outros campos de avaliação
            estagio.empresa_nota_interesse = form.empresa_nota_interesse.data
            estagio.empresa_nota_iniciativa = form.empresa_nota_iniciativa.data
            estagio.empresa_nota_cooperacao = form.empresa_nota_cooperacao.data
            estagio.empresa_nota_assiduidade = form.empresa_nota_assiduidade.data
            estagio.empresa_nota_pontualidade = form.empresa_nota_pontualidade.data
            estagio.empresa_nota_disciplina = form.empresa_nota_disciplina.data
            estagio.empresa_nota_sociabilidade = form.empresa_nota_sociabilidade.data
            estagio.empresa_nota_adaptabilidade = form.empresa_nota_adaptabilidade.data
            estagio.empresa_nota_responsabilidade = form.empresa_nota_responsabilidade.data
            estagio.empresa_nota_etica = form.empresa_nota_etica.data
            estagio.empresa_atividades = form.empresa_atividades.data
            estagio.emprsa_comentarios = form.emprsa_comentarios.data
            
            # Calcula a média das notas
            estagio.empresa_media_notas = sum([
                form.empresa_nota_interesse.data,
                form.empresa_nota_iniciativa.data,
                form.empresa_nota_cooperacao.data,
                form.empresa_nota_assiduidade.data,
                form.empresa_nota_pontualidade.data,
                form.empresa_nota_disciplina.data,
                form.empresa_nota_sociabilidade.data,
                form.empresa_nota_adaptabilidade.data,
                form.empresa_nota_responsabilidade.data,
                form.empresa_nota_etica.data
            ]) / 10
            
            estagio.banca_nota_avaliacao_empresa = estagio.empresa_media_notas
            
            db.session.commit()
            flash('Avaliação salva com sucesso!', 'success')
            return redirect(url_for('index_empresa'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar avaliação: {e}', 'error')

    return render_template('empresa/avaliacao_empresa.html', form=form, estagio=estagio)

# Fim Area Empresa

# Inicio Area Supervisor

@app.route('/home-supervisor', methods=['GET'])
@roles_required('supervisor')
def index_supervisor():
    estagios = Estagio.query.join(Supervisor, Estagio.supervisor_id == Supervisor.id) \
                        .filter(Supervisor.user_id == current_user.id).all()
    
    return render_template('supervisor/index_supervisor.html', estagios=estagios)

@app.route('/supervisor/avaliacao/<int:estagio_id>', methods=['GET', 'POST'])
@roles_required('supervisor')
def avaliacao_supervisor(estagio_id):
    # Busca o estágio específico vinculado à empresa atual
    estagio = Estagio.query.join(Supervisor).filter(
        Estagio.id == estagio_id,
        Supervisor.user_id == current_user.id
    ).first_or_404()

    form = SupervisorAvaliacaoForm(obj=estagio)
    
    if form.validate_on_submit():
        try:
            # Atualiza as notas e outros campos de avaliação
            estagio.supervisor_nota_interesse = form.supervisor_nota_interesse.data
            estagio.supervisor_nota_iniciativa = form.supervisor_nota_iniciativa.data
            estagio.supervisor_nota_cooperacao = form.supervisor_nota_cooperacao.data
            estagio.supervisor_nota_assiduidade_e_pontuabilidade = form.supervisor_nota_assiduidade_e_pontuabilidade.data
            estagio.supervisor_nota_criatividade_e_engenhosidade = form.supervisor_nota_criatividade_e_engenhosidade.data
            estagio.supervisor_nota_disciplina = form.supervisor_nota_disciplina.data
            estagio.supervisor_nota_sociabilidade = form.supervisor_nota_sociabilidade.data
            estagio.supervisor_nota_adaptabilidade = form.supervisor_nota_adaptabilidade.data
            estagio.supervisor_nota_responsabilidade = form.supervisor_nota_responsabilidade.data
            estagio.supervisor_evolucao_tecnica = form.supervisor_evolucao_tecnica.data
            estagio.supervisor_nota_etica = form.supervisor_nota_etica.data
            estagio.supervisor_atividades = form.supervisor_atividades.data
            estagio.supervisor_comentarios = form.supervisor_comentarios.data
            
            # Calcula a média das notas
            notas = [
                form.supervisor_nota_interesse.data,
                form.supervisor_nota_iniciativa.data,
                form.supervisor_nota_cooperacao.data,
                form.supervisor_nota_assiduidade_e_pontuabilidade.data,
                form.supervisor_nota_criatividade_e_engenhosidade.data,
                form.supervisor_nota_disciplina.data,
                form.supervisor_nota_sociabilidade.data,
                form.supervisor_nota_adaptabilidade.data,
                form.supervisor_nota_responsabilidade.data,
                form.supervisor_evolucao_tecnica.data,
                form.supervisor_nota_etica.data
            ]
            
            estagio.supervisor_media_notas = sum(filter(None, notas)) / len([n for n in notas if n is not None])
            estagio.banca_nota_avaliacao_orientador = estagio.supervisor_media_notas

            db.session.commit()
            flash('Avaliação salva com sucesso!', 'success')
            return redirect(url_for('index_supervisor'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar avaliação: {e}', 'error')
            
    return render_template('supervisor/avaliacao_supervisor.html', form=form, estagio=estagio)

# Fim Area Supervisor

# Area Professor

@app.route('/home-professor', methods=['GET'])
@roles_required('professor')
def index_professor():
    estagios = Estagio.query.join(Professor, Estagio.professor_id == Professor.id) \
                        .filter(Professor.user_id == current_user.id).all()
    
    return render_template('professor/index_professor.html', estagios=estagios)

@app.route('/professor/avaliacao/<int:estagio_id>', methods=['GET', 'POST'])
@roles_required('professor')
def avaliacao_professor(estagio_id):
    estagio = Estagio.query.join(Professor).filter(
        Estagio.id == estagio_id,
        Professor.user_id == current_user.id
    ).first_or_404()

    form = ProfessorAvaliacaoForm(obj=estagio)
    if form.validate_on_submit():
        try:
            # Atualiza as notas e outros campos de avaliação
            estagio.professor_nota_avaliacao = form.professor_nota_avaliacao.data
            estagio.professor_avaliacao_comentarios = form.professor_avaliacao_comentarios.data

            db.session.commit()
            flash('Avaliação salva com sucesso!', 'success')
            return redirect(url_for('index_professor'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar avaliação: {e}', 'error')
            
    return render_template('professor/avaliacao_professor.html', form=form, estagio=estagio)

@app.route('/banca/avaliacao/<int:estagio_id>', methods=['GET', 'POST'])
@roles_required('professor')
def notas_banca(estagio_id):
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()

    form = BancaAvaliacaoForm(obj=estagio)
    
    if form.validate_on_submit():
        try:
            estagio.banca_nota_apresentacao_oral_1 = form.banca_nota_apresentacao_oral_1.data
            estagio.banca_nota_pratica_profissional_1 = form.banca_nota_pratica_profissional_1.data
            estagio.banca_nota_relatorio_1 = form.banca_nota_relatorio_1.data
            estagio.banca_nota_apresentacao_oral_2 = form.banca_nota_apresentacao_oral_2.data
            estagio.banca_nota_pratica_profissional_2 = form.banca_nota_pratica_profissional_2.data
            estagio.banca_nota_relatorio_2 = form.banca_nota_relatorio_2.data
            estagio.banca_nota_apresentacao_oral_supervisor = form.banca_nota_apresentacao_oral_supervisor.data
            estagio.banca_nota_pratica_profissional_supervisor = form.banca_nota_pratica_profissional_supervisor.data
            estagio.banca_nota_relatorio_supervisor = form.banca_nota_relatorio_supervisor.data
            estagio.banca_avaliador_1 = form.banca_avaliador_1.data
            estagio.banca_avaliador_2 = form.banca_avaliador_2.data
            estagio.banca_aprovado = form.banca_aprovado.data
            estagio.banca_reprovado = form.banca_reprovado.data
            estagio.banca_aprovado_com_ressalva = form.banca_aprovado_com_ressalva.data
            estagio.banca_relatorio_entrega = form.banca_relatorio_entrega.data
            estagio.banca_refazer_apresentacao = form.banca_refazer_apresentacao.data
            estagio.banca_comentarios = form.banca_comentarios.data

            db.session.commit()
            flash('Avaliação da banca salva com sucesso!', 'success')
            return redirect(url_for('index_professor'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar avaliação: {e}', 'error')
    
    return render_template('professor/notas_banca.html', form=form, estagio=estagio)
# Fim Area Professor

# Area Aluno

@app.route('/home-aluno', methods=['GET', 'POST'])
@roles_required('aluno')
def index_aluno():
    aluno = Aluno.query.filter_by(user_id=current_user.id).first_or_404()
    estagio = Estagio.query.filter_by(aluno_id=aluno.id).first()
    
    if estagio:  # Se o aluno já possui um estágio, mostrar os dados do estágio para edição
        form = EstagioFormAdd(obj=estagio)
        form.estagio_id = estagio.id
        form.professor_id.choices = [
            (p.id, p.nome) for p in Professor.query.join(Professor.user).filter(
                or_(
                    Professor.id == estagio.professor_id,
                    and_(Professor.is_approved == True, User.active == True)
                )
            ).all()
        ]

        form.supervisor_id.choices = [
            (s.id, s.nome) for s in Supervisor.query.join(Supervisor.user).filter(
                or_(
                    Supervisor.id == estagio.supervisor_id,
                    and_(Supervisor.is_approved == True, User.active == True)
                )
            ).all()
        ]

        form.empresa_id.choices = [
            (e.id, e.nome_empresa) for e in Empresa.query.join(Empresa.user).filter(
                or_(
                    Empresa.id == estagio.empresa_id,
                    and_(Empresa.is_approved == True, User.active == True)
                )
            ).all()
        ]

        if request.method == 'GET':
            form.professor_id.data = estagio.professor_id
            form.supervisor_id.data = estagio.supervisor_id
            form.empresa_id.data = estagio.empresa_id

        if form.validate_on_submit():
            try:
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

                db.session.merge(estagio)
                db.session.commit()
                flash('Estágio atualizado com sucesso!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar estágio: {e}', 'error')
    else:  # Se o aluno não possui um estágio, permitir o cadastro
        form = EstagioFormAdd()
        form.professor_id.choices = [
            (p.id, p.nome) for p in Professor.query.join(Professor.user).filter(Professor.is_approved == True, User.active == True).all()
        ]

        form.supervisor_id.choices = [
            (s.id, s.nome) for s in Supervisor.query.join(Supervisor.user).filter(Supervisor.is_approved == True, User.active == True).all()
        ]

        form.empresa_id.choices = [
            (e.id, e.nome_empresa) for e in Empresa.query.join(Empresa.user).filter(Empresa.is_approved == True, User.active == True).all()
        ]

        if form.validate_on_submit():
            try:
                estagio = Estagio(
                    aluno_id=aluno.id,
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
                    is_approved=False,
                    status=StatusEstagio.AGUARDANDO_APROVACAO
                )

                db.session.add(estagio)
                db.session.commit()

                flash('Estágio cadastrado com sucesso!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar estágio. Error: {str(e)}', 'error')

    return render_template('aluno/cadastro_estagio.html', form=form, aluno=aluno)

@app.route('/auto-avaliacao', methods=['GET', 'POST'])
@roles_required('aluno')
def auto_avaliacao():
    aluno = Aluno.query.filter_by(user_id=current_user.id).first_or_404()
    estagio = Estagio.query.filter_by(aluno_id=aluno.id).first_or_404()

    form = AutoAvaliacaoForm(obj=estagio)

    if form.validate_on_submit():
        try:
            estagio.aluno_nota_rendimento = form.aluno_nota_rendimento.data
            estagio.aluno_nota_facilidade_e_compreensao = form.aluno_nota_facilidade_e_compreensao.data
            estagio.aluno_nota_conhecimentos_tecnicos = form.aluno_nota_conhecimentos_tecnicos.data
            estagio.aluno_nota_organizacao_metodo_trabalho = form.aluno_nota_organizacao_metodo_trabalho.data
            estagio.aluno_nota_iniciativa_independencia = form.aluno_nota_iniciativa_independencia.data
            estagio.aluno_nota_disciplina = form.aluno_nota_disciplina.data
            estagio.aluno_nota_sociabilidade_desempenho = form.aluno_nota_sociabilidade_desempenho.data
            estagio.aluno_nota_assiduidade = form.aluno_nota_assiduidade.data
            estagio.aluno_nota_cooperecao = form.aluno_nota_cooperecao.data
            estagio.aluno_nota_responsabilidade = form.aluno_nota_responsabilidade.data
            estagio.aluno_atividades = form.aluno_atividades.data
            estagio.aluno_comentarios = form.aluno_comentarios.data
            estagio.aluno_avaliacao_empresa_condicoes = form.aluno_avaliacao_empresa_condicoes.data
            estagio.aluno_avaliacao_atendeu_expectativas = form.aluno_avaliacao_atendeu_expectativas.data
            estagio.aluno_avaliacao_contribui_formacao_profissional = form.aluno_avaliacao_contribui_formacao_profissional.data
            estagio.aluno_avaliacao_recomendaria_para_outro = form.aluno_avaliacao_recomendaria_para_outro.data
            estagio.aluno_avaliacao_curso_capacitou = form.aluno_avaliacao_curso_capacitou.data
            estagio.aluno_avaliacao_orientador_acompanhou = form.aluno_avaliacao_orientador_acompanhou.data
            estagio.aluno_avaliacao_supervisor_acompanhou = form.aluno_avaliacao_supervisor_acompanhou.data

            # Calcula a média das notas numéricas
            notas = [
                form.aluno_nota_rendimento.data,
                form.aluno_nota_facilidade_e_compreensao.data,
                form.aluno_nota_conhecimentos_tecnicos.data,
                form.aluno_nota_organizacao_metodo_trabalho.data,
                form.aluno_nota_iniciativa_independencia.data,
                form.aluno_nota_disciplina.data,
                form.aluno_nota_sociabilidade_desempenho.data,
                form.aluno_nota_assiduidade.data,
                form.aluno_nota_cooperecao.data,
                form.aluno_nota_responsabilidade.data
            ]
            estagio.aluno_media_notas = sum(filter(None, notas)) / len([n for n in notas if n is not None])

            db.session.commit()
            flash('Autoavaliação salva com sucesso!', 'success')
            return redirect(url_for('index_aluno'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar autoavaliação: {str(e)}', 'error')

    return render_template('aluno/autoavaliacao.html', form=form)

@app.route('/aluno/cadastrar-atividade', methods=['GET', 'POST'])
@roles_required('aluno')
def cadastrar_atividade_estagio():
    aluno = Aluno.query.filter_by(user_id=current_user.id).first_or_404()
    estagio = Estagio.query.filter_by(aluno_id=aluno.id).first_or_404()
    
    form = AtividadesEstagioForm()
    form.estagio_id.data = estagio.id  # Preenche automaticamente o ID do estágio no formulário

    if form.validate_on_submit():
        try:
            atividade = AtividadesEstagio(
                descricao=form.descricao.data,
                data=form.data.data,
                horario_entrada=form.horario_entrada.data,
                horario_saida=form.horario_saida.data,
                horas_totais=form.horas_totais.data,
                estagio_id=estagio.id
            )
            db.session.add(atividade)
            db.session.commit()
            
            flash('Atividade cadastrada com sucesso!', 'success')
            return redirect(url_for('index_aluno'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar atividade: {str(e)}', 'error')

    return render_template('aluno/cadastro_atividade.html', form=form)

@app.route('/aluno/listar-atividades', methods=['GET'])
@roles_required('aluno')
def listar_atividades_estagio():
    aluno = Aluno.query.filter_by(user_id=current_user.id).first_or_404()
    estagio = Estagio.query.filter_by(aluno_id=aluno.id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    return render_template('aluno/listagem_atividades.html', atividades=atividades, estagio=estagio)

@app.route('/aluno/editar-atividade/<int:atividade_id>', methods=['GET', 'POST'])
@roles_required('aluno')
def editar_atividade_estagio(atividade_id):
    atividade = AtividadesEstagio.query.filter_by(id=atividade_id).first_or_404()
    aluno = Aluno.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Verificar se a atividade pertence ao estágio do aluno atual
    estagio = Estagio.query.filter_by(aluno_id=aluno.id).first_or_404()
    if atividade.estagio_id != estagio.id:
        flash('Você não tem permissão para editar essa atividade.', 'error')
        return redirect(url_for('listar_atividades_estagio'))

    form = AtividadesEstagioForm(obj=atividade)
    
    if form.validate_on_submit():
        try:
            atividade.descricao = form.descricao.data
            atividade.data = form.data.data
            atividade.horario_entrada = form.horario_entrada.data
            atividade.horario_saida = form.horario_saida.data
            atividade.horas_totais = form.horas_totais.data

            db.session.commit()
            flash('Atividade editada com sucesso!', 'success')
            return redirect(url_for('listar_atividades_estagio'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao editar atividade: {str(e)}', 'error')
    
    return render_template('aluno/editar_atividade.html', form=form, atividade=atividade)

@app.route('/listar-atividades-empresa/<int:estagio_id>', methods=['GET'])
def listar_atividades_empresa(estagio_id):
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    return render_template('aluno/listagem_atividades_empresa.html', atividades=atividades, estagio=estagio)

@app.route('/listar-atividades-supervisor/<int:estagio_id>', methods=['GET'])
def listar_atividades_supervisor(estagio_id):
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    return render_template('aluno/listagem_atividades_supervisor.html', atividades=atividades, estagio=estagio)

@app.route('/listar-atividades-professor/<int:estagio_id>', methods=['GET'])
def listar_atividades_professor(estagio_id):
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    return render_template('aluno/listagem_atividades_professor.html', atividades=atividades, estagio=estagio)

@app.route('/listar-atividades-admin/<int:estagio_id>', methods=['GET'])
def listar_atividades_admin(estagio_id):
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    return render_template('aluno/listagem_atividades_admin.html', atividades=atividades, estagio=estagio)

# Fim Area Aluno

# Area criação de PDFs

@app.route('/generate_company_pdf/<int:estagio_id>', methods=['GET'])
def generate_company_pdf(estagio_id):
    # Fetch internship (Estagio) details
    estagio = Estagio.query.join(Empresa).filter(Estagio.id == estagio_id).first_or_404()
    
    data_inicio_formatada = estagio.data_inicio.strftime('%d/%m/%Y') if estagio.data_inicio else ''
    data_conclusao_formatada = estagio.data_conclusao.strftime('%d/%m/%Y') if estagio.data_conclusao else ''

    # Populate data dictionary with relevant fields
    data_dict = {
        'nome_estagiario': estagio.aluno.nome,
        'nome_empresa': estagio.empresa.nome_empresa,
        'nome_curso': 'Informática',
        'periodo': f"{data_inicio_formatada} - {data_conclusao_formatada}",
        'nota_interesse': str(estagio.empresa_nota_interesse or ''),
        'nota_iniciativa': str(estagio.empresa_nota_iniciativa or ''),
        'nota_cooperacao': str(estagio.empresa_nota_cooperacao or ''),
        'nota_assiduidade': str(estagio.empresa_nota_assiduidade or ''),
        'nota_pontualidade': str(estagio.empresa_nota_pontualidade or ''),
        'nota_disciplina': str(estagio.empresa_nota_disciplina or ''),
        'nota_sociabilidade': str(estagio.empresa_nota_sociabilidade or ''),
        'nota_adaptabilidade': str(estagio.empresa_nota_adaptabilidade or ''),
        'nota_responsabilidade': str(estagio.empresa_nota_responsabilidade or ''),
        'nota_etica': str(estagio.empresa_nota_etica or ''),
        'nota_media': str(estagio.empresa_media_notas or ''),
        'atividades': estagio.empresa_atividades or '',
        'observacoes': estagio.emprsa_comentarios or ''
    }

    base_dir = os.path.dirname(__file__)
    input_pdf_path = os.path.join(base_dir, 'Files', 'avaliacao_empresa_editavel.pdf')
    
    doc = fitz.open(input_pdf_path)
    
    title = f"Avaliação Empresa - {estagio.empresa.nome_empresa} - Aluno {estagio.aluno.nome}"
    doc.set_metadata({"title": title})
    
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for field in widgets:
                field_name = field.field_name
                if field_name in data_dict:
                    field.text_color = (0, 0, 0)  # Define a cor do texto como preto (RGB)
                    field.font_size = 12  # Define o tamanho da fonte
                    field.field_value = data_dict[field_name]
                    field.update()

    for page in doc:
        page.clean_contents()

    pdf_stream = BytesIO()
    doc.save(pdf_stream, incremental=False, deflate=True)
    pdf_stream.seek(0)
    
    return send_file(pdf_stream, as_attachment=True, download_name=f"Avaliacao_Empresa_{estagio.empresa.nome_empresa}_Aluno_{estagio.aluno.nome}.pdf", mimetype='application/pdf')

@app.route('/generate_professor_pdf/<int:estagio_id>', methods=['GET'])
def generate_professor_pdf(estagio_id):
    estagio = Estagio.query.join(Professor).filter(Estagio.id == estagio_id).first_or_404()

    data_dict = {
        'nome_estagiario': estagio.aluno.nome,
        'nome_empresa': estagio.empresa.nome_empresa,
        'nota': str(estagio.professor_nota_avaliacao or ''),
        'comentarios': estagio.professor_avaliacao_comentarios or '',
    }

    base_dir = os.path.dirname(__file__)
    input_pdf_path = os.path.join(base_dir, 'Files', 'avaliacao_professor_editavel.pdf')
    
    doc = fitz.open(input_pdf_path)
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for field in widgets:
                field_name = field.field_name
                if field_name in data_dict:
                    field.field_value = data_dict[field_name]
                    field.update()

    title = f"Avaliação Professor - {estagio.professor.nome} - Aluno {estagio.aluno.nome}"
    doc.set_metadata({"title": title})

    for page in doc:
        page.clean_contents()

    pdf_stream = BytesIO()
    doc.save(pdf_stream, incremental=False, deflate=True)
    pdf_stream.seek(0)
    
    return send_file(pdf_stream, as_attachment=True, download_name=f"Avaliacao_Professor_{estagio.professor.nome}_Aluno_{estagio.aluno.nome}.pdf", mimetype='application/pdf')

@app.route('/generate_self_evaluation_pdf/<int:estagio_id>', methods=['GET'])
def generate_self_evaluation_pdf(estagio_id):
    estagio = Estagio.query.filter(Estagio.id == estagio_id).first_or_404()

    data_inicio_formatada = estagio.data_inicio.strftime('%d/%m/%Y') if estagio.data_inicio else ''
    data_conclusao_formatada = estagio.data_conclusao.strftime('%d/%m/%Y') if estagio.data_conclusao else ''
    
    data_dict = {
        'nome_estagiario': estagio.aluno.nome,
        'nome_empresa': estagio.empresa.nome_empresa,
        'periodo': f"{data_inicio_formatada} - {data_conclusao_formatada}",
        'nota_rendimento': str(estagio.aluno_nota_rendimento or ''),
        'nota_compreensao': str(estagio.aluno_nota_facilidade_e_compreensao or ''),
        'nota_conhecimentos': str(estagio.aluno_nota_conhecimentos_tecnicos or ''),
        'nota_organizacao': str(estagio.aluno_nota_organizacao_metodo_trabalho or ''),
        'nota_iniciativa': str(estagio.aluno_nota_iniciativa_independencia or ''),
        'nota_assiduidade': str(estagio.aluno_nota_assiduidade or ''),
        'nota_disciplina': str(estagio.aluno_nota_disciplina or ''),
        'nota_sociabilidade': str(estagio.aluno_nota_sociabilidade_desempenho or ''),
        'nota_cooperacao': str(estagio.aluno_nota_cooperecao or ''),
        'nota_responsabilidade': str(estagio.aluno_nota_responsabilidade or ''),
        'media_nota': str(estagio.aluno_media_notas or ''),
        'atividades': estagio.aluno_atividades or '',
        'comentarios': estagio.aluno_comentarios or ''
    }

    def map_checkbox_value(value, field_name_prefix):
        return {
            f"{field_name_prefix}_sim": 'Yes' if value == 1 else '',
            f"{field_name_prefix}_nao": 'Yes' if value == 2 else '',
            f"{field_name_prefix}_medio": 'Yes' if value == 3 else '',
        }

    checkbox_fields = {
        **map_checkbox_value(estagio.aluno_avaliacao_empresa_condicoes, 'condicoes'),
        **map_checkbox_value(estagio.aluno_avaliacao_atendeu_expectativas, 'expectativa'),
        **map_checkbox_value(estagio.aluno_avaliacao_contribui_formacao_profissional, 'contribuiu'),
        **map_checkbox_value(estagio.aluno_avaliacao_recomendaria_para_outro, 'recomendaria'),
        **map_checkbox_value(estagio.aluno_avaliacao_curso_capacitou, 'capacitou'),
        **map_checkbox_value(estagio.aluno_avaliacao_orientador_acompanhou, 'orientador_acompanhou'),
        **map_checkbox_value(estagio.aluno_avaliacao_supervisor_acompanhou, 'supervisor_acompanhou'),
    }

    data_dict.update(checkbox_fields)

    base_dir = os.path.dirname(__file__)
    input_pdf_path = os.path.join(base_dir, 'Files', 'autoavaliacao_editavel.pdf')

    doc = fitz.open(input_pdf_path)
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for field in widgets:
                field_name = field.field_name
                if field_name in data_dict:
                    field.field_value = data_dict[field_name]
                    field.update()

    title = f"Autoavaliação Estagiário - {estagio.aluno.nome}"
    doc.set_metadata({"title": title})

    for page in doc:
        page.clean_contents()

    pdf_stream = BytesIO()
    doc.save(pdf_stream, incremental=False, deflate=True)
    pdf_stream.seek(0)

    return send_file(pdf_stream, as_attachment=True, download_name=f"Autoavaliacao_Estagiario_{estagio.aluno.nome}.pdf", mimetype='application/pdf')

@app.route('/generate_ata_banca_pdf/<int:estagio_id>', methods=['GET'])
def generate_ata_banca_pdf(estagio_id):
    # Buscar detalhes do estágio (Estagio)
    estagio = Estagio.query.filter(Estagio.id == estagio_id).first_or_404()

    # Calcular médias e valores derivados
    avaliacao_concedente_peso = (estagio.banca_nota_avaliacao_empresa or 0) * 2
    avaliacao_orientador_peso = (estagio.banca_nota_avaliacao_orientador or 0) * 2
    
    apresentacao_oral_n1 = estagio.banca_nota_apresentacao_oral_supervisor or 0
    apresentacao_oral_n2 = estagio.banca_nota_apresentacao_oral_1 or 0
    apresentacao_oral_n3 = estagio.banca_nota_apresentacao_oral_2 or 0
    apresentacao_oral_media = (apresentacao_oral_n1 + apresentacao_oral_n2 + apresentacao_oral_n3) / 3
    apresentacao_oral_media_peso = apresentacao_oral_media * 2

    pratica_profissional_n1 = estagio.banca_nota_pratica_profissional_supervisor or 0
    pratica_profissional_n2 = estagio.banca_nota_pratica_profissional_1 or 0
    pratica_profissional_n3 = estagio.banca_nota_pratica_profissional_2 or 0
    pratica_profissional_media = (pratica_profissional_n1 + pratica_profissional_n2 + pratica_profissional_n3) / 3
    pratica_profissional_media_peso = pratica_profissional_media * 2

    relatorio_descritivo_n1 = estagio.banca_nota_relatorio_supervisor or 0
    relatorio_descritivo_n2 = estagio.banca_nota_relatorio_1 or 0
    relatorio_descritivo_n3 = estagio.banca_nota_relatorio_2 or 0
    relatorio_descritivo_media = (relatorio_descritivo_n1 + relatorio_descritivo_n2 + relatorio_descritivo_n3) / 3
    relatorio_descritivo_media_peso = relatorio_descritivo_media  # Mesma média

    autoavaliacao = estagio.banca_autoavaliacao or 0
    autoavaliacao_peso = autoavaliacao  # Mesma nota

    # Calculando nota final
    nota_final = (
        avaliacao_concedente_peso +
        avaliacao_orientador_peso +
        apresentacao_oral_media_peso +
        pratica_profissional_media_peso +
        relatorio_descritivo_media_peso +
        autoavaliacao_peso
    )

    # Formatar as datas no formato dia/mês/ano
    data_relatorio = estagio.banca_relatorio_entrega.strftime('%d/%m/%Y') if estagio.banca_relatorio_entrega else ''
    data_apresentacao = estagio.banca_refazer_apresentacao.strftime('%d/%m/%Y') if estagio.banca_refazer_apresentacao else ''
    ano = estagio.banca_relatorio_entrega.year if estagio.banca_relatorio_entrega else estagio.banca_refazer_apresentacao.year if estagio.banca_refazer_apresentacao else ''

    # Criar o dicionário com os dados a serem preenchidos
    data_dict = {
        'avaliacao_concedente': str(estagio.banca_nota_avaliacao_empresa or ''),
        'avaliacao_concedente_peso': str(avaliacao_concedente_peso),
        'avaliacao_orientador': str(estagio.banca_nota_avaliacao_orientador or ''),
        'avaliacao_orientador_peso': str(avaliacao_orientador_peso),
        'apresentacao_oral_n1': str(apresentacao_oral_n1),
        'apresentacao_oral_n2': str(apresentacao_oral_n2),
        'apresentacao_oral_n3': str(apresentacao_oral_n3),
        'apresentacao_oral_media': str(apresentacao_oral_media),
        'apresentacao_oral_media_peso': str(apresentacao_oral_media_peso),
        'pratica_profissional_n1': str(pratica_profissional_n1),
        'pratica_profissional_n2': str(pratica_profissional_n2),
        'pratica_profissional_n3': str(pratica_profissional_n3),
        'pratica_profissional_media': str(pratica_profissional_media),
        'pratica_profissional_media_peso': str(pratica_profissional_media_peso),
        'relatorio_descritivo_n1': str(relatorio_descritivo_n1),
        'relatorio_descritivo_n2': str(relatorio_descritivo_n2),
        'relatorio_descritivo_n3': str(relatorio_descritivo_n3),
        'relatorio_descritivo_media': str(relatorio_descritivo_media),
        'relatorio_descritivo_media_peso': str(relatorio_descritivo_media_peso),
        'autoavalicao': str(autoavaliacao),
        'autoavalicao_peso': str(autoavaliacao_peso),
        'nota_final': str(nota_final),
        'data_relatorio': data_relatorio,
        'data_apresentacao': data_apresentacao,
        'ano': str(ano),
        'comentarios': estagio.banca_comentarios or '',
        'nome_avaliador1': estagio.banca_avaliador_1 or '',
        'nome_avaliador2': estagio.banca_avaliador_2 or '',
        'orientador': estagio.professor.nome,
    }

    # Campos de checkbox
    data_dict.update({
        'aprovado': 'Yes' if estagio.banca_aprovado else '',
        'aprovado_ressalva': 'Yes' if estagio.banca_aprovado_com_ressalva else '',
        'reprovado': 'Yes' if estagio.banca_reprovado else '',
    })

    # Caminho do PDF editável
    base_dir = os.path.dirname(__file__)
    input_pdf_path = os.path.join(base_dir, 'Files', 'ata_banca_editavel.pdf')

    # Abrir e preencher o PDF
    doc = fitz.open(input_pdf_path)
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for field in widgets:
                field_name = field.field_name
                if field_name in data_dict:
                    field.field_value = data_dict[field_name]
                    field.update()

    # Atualizar os metadados do PDF
    title = f"Ata Banca - {estagio.aluno.nome}"
    doc.set_metadata({"title": title})

    # Remover os campos de formulário para "flatten" o PDF
    for page in doc:
        page.clean_contents()

    # Salvar o PDF em memória usando BytesIO
    pdf_stream = BytesIO()
    doc.save(pdf_stream, incremental=False, deflate=True)
    pdf_stream.seek(0)

    return send_file(pdf_stream, as_attachment=True, download_name=f"Ata_Banca_{estagio.aluno.nome}.pdf", mimetype='application/pdf')

import zipfile
import locale

@app.route('/generate_atividades_estagio_pdf/<int:estagio_id>', methods=['GET'])
def generate_atividades_estagio_pdf(estagio_id):
    # Set locale to Portuguese for month names
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

    # Fetch internship (Estagio) details and its activities
    estagio = Estagio.query.filter_by(id=estagio_id).first_or_404()
    atividades = AtividadesEstagio.query.filter_by(estagio_id=estagio.id).all()

    # Group activities by month and year
    atividades_por_mes = {}
    for atividade in atividades:
        mes_ano = atividade.data.strftime('%Y-%m')
        if mes_ano not in atividades_por_mes:
            atividades_por_mes[mes_ano] = []
        atividades_por_mes[mes_ano].append(atividade)

    base_dir = os.path.dirname(__file__)
    input_pdf_path = os.path.join(base_dir, 'Files', 'atividades_estagio_editavel.pdf')

    pdf_files = []

    for mes_ano, atividades_mes in atividades_por_mes.items():
        # Prepare data for the PDF
        nome_mes_pt = atividades_mes[0].data.strftime('%B/%Y').capitalize()
        data_dict = {
            'nome_estagiario': estagio.aluno.nome,
            'nome_empresa': estagio.empresa.nome_empresa,
            'nome_mes': nome_mes_pt,
            'nome_mes2': nome_mes_pt,
            'nome_empresa2': estagio.empresa.nome_empresa,
            'nome_estagiario2': estagio.aluno.nome,
            'observacoes': ''  # Add any observations if needed
        }

        # Fill in the fields for each day of the month
        for atividade in atividades_mes:
            dia = atividade.data.day
            data_dict[f'entrada_{dia:02d}'] = atividade.horario_entrada.strftime('%H:%M')
            data_dict[f'saida_{dia:02d}'] = atividade.horario_saida.strftime('%H:%M')
            data_dict[f'horas_{dia:02d}'] = str(atividade.horas_totais)
            data_dict[f'descricao_{dia:02d}'] = atividade.descricao

        # Open and fill the PDF template
        doc = fitz.open(input_pdf_path)
        for page in doc:
            widgets = page.widgets()
            if widgets:
                for field in widgets:
                    field_name = field.field_name
                    if field_name in data_dict:
                        field.field_value = data_dict[field_name]
                        field.update()

        # Update metadata and flatten the PDF
        title = f"Atividades Estágio - {nome_mes_pt} - {estagio.aluno.nome}"
        doc.set_metadata({"title": title})
        for page in doc:
            page.clean_contents()

        # Save the PDF to memory
        pdf_stream = BytesIO()
        doc.save(pdf_stream, incremental=False, deflate=True)
        pdf_stream.seek(0)

        # Add the PDF stream to the list
        pdf_files.append((pdf_stream, f"Atividades_Estagio_{nome_mes_pt}_{estagio.aluno.nome}.pdf"))

    # Create a response with multiple PDF files
    if len(pdf_files) == 1:
        # If there's only one file, return it directly
        return send_file(pdf_files[0][0], as_attachment=True, download_name=pdf_files[0][1], mimetype='application/pdf')
    else:
        # If there are multiple files, create a zip
        zip_stream = BytesIO()
        with zipfile.ZipFile(zip_stream, 'w') as zip_file:
            for pdf_stream, filename in pdf_files:
                zip_file.writestr(filename, pdf_stream.read())
        zip_stream.seek(0)
        return send_file(zip_stream, as_attachment=True, download_name=f"Atividades_Estagio_{estagio.aluno.nome}.zip", mimetype='application/zip')

    
# Fim Area criação de PDFs