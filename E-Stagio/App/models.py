import uuid
from datetime import datetime, date
from app import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.types import Enum as SQLEnum
import enum

# Tabela associativa para a relação muitos-para-muitos entre User e Role
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())  # Campo para armazenar a data/hora da confirmação do e-mail
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))  # Relação muitos-para-muitos com Role
    current_login_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_ip = db.Column(db.String(100))
    last_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária autoincrementável
    cnpj = db.Column(db.String(18), unique=True, nullable=False)  # CNPJ como campo único
    qsa = db.Column(db.String(255), nullable=False)  # QSA é opcional
    rg_responsavel = db.Column(db.String(20), nullable=False)  # RG do responsável
    cpf_responsavel = db.Column(db.String(14), nullable=False)  # CPF do responsável
    nome_empresa = db.Column(db.String(100), nullable=False)  # Nome da empresa
    nome_responsavel = db.Column(db.String(100), nullable=False)  # Nome do responsável
    email_empresa = db.Column(db.String(100), nullable=False)  # Email da empresa
    email_responsavel = db.Column(db.String(100), nullable=True)  # Email do responsável
    telefone_empresa = db.Column(db.String(20), nullable=False)  # Telefone da empresa
    telefone_responsavel = db.Column(db.String(20), nullable=True)  # Telefone do responsável
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_approved = db.Column(db.Boolean())
    
    user = db.relationship('User', backref=db.backref('empresas', lazy=True))

    def __repr__(self):
        return f'<Empresa {self.nome_empresa}>'

class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)  # Automatic primary key
    nome = db.Column(db.String(100), nullable=False)  # Nome do professor
    email = db.Column(db.String(100), unique=False, nullable=False)  # Email must be unique
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # Formatted CPF with uniqueness
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_approved = db.Column(db.Boolean())

    user = db.relationship('User', backref=db.backref('professores', lazy=True))
    
    def __repr__(self):
        return f'<Professor {self.nome}>'
    
class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)  # Automatic primary key
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    data_de_nascimento = db.Column(db.Date, nullable=False)
    rg = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_approved = db.Column(db.Boolean())
    
    user = db.relationship('User', backref=db.backref('alunos', lazy=True))
    
    def __repr__(self):
        return f'<Aluno {self.nome}>'
    
class Supervisor(db.Model):
    __tablename__ = 'supervisores'

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    formacao = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_approved = db.Column(db.Boolean())

    empresa = db.relationship('Empresa', backref=db.backref('supervisores', lazy=True))
    user = db.relationship('User', backref=db.backref('supervisor', lazy=True))
    
    def __repr__(self):
        return f'<Supervisor {self.nome}>'

class StatusEstagio(enum.Enum):
    AGUARDANDO_APROVACAO = 'aguardando_aprovacao'
    APROVADO = 'aprovado'
    EM_ANDAMENTO = 'em_andamento'
    AGUARDANDO_AVALIACAO = 'aguardando_avaliacao'
    FINALIZADO = 'finalizado'
    CANCELADO = 'cancelado'

class Estagio(db.Model):
    __tablename__ = 'estagios'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisores.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    modalidade = db.Column(db.String(50), nullable=False)
    carga_horaria = db.Column(db.Integer, nullable=False)
    atividades = db.Column(db.Text, nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    remuneracao = db.Column(db.Boolean, nullable=False)
    valor_remuneracao = db.Column(db.Float, nullable=True)  # Pode ser nulo se não houver remuneração
    horario_estagio = db.Column(db.String(100), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_conclusao = db.Column(db.Date, nullable=False)
    is_approved = db.Column(db.Boolean())
    status = db.Column(SQLEnum(StatusEstagio), default=StatusEstagio.AGUARDANDO_APROVACAO, nullable=False)
    
    empresa_nota_interesse = db.Column(db.Float, nullable=True)
    empresa_nota_iniciativa = db.Column(db.Float, nullable=True)
    empresa_nota_cooperacao = db.Column(db.Float, nullable=True)
    empresa_nota_assiduidade = db.Column(db.Float, nullable=True)
    empresa_nota_pontualidade = db.Column(db.Float, nullable=True)
    empresa_nota_disciplina = db.Column(db.Float, nullable=True)
    empresa_nota_sociabilidade = db.Column(db.Float, nullable=True)
    empresa_nota_adaptabilidade = db.Column(db.Float, nullable=True)
    empresa_nota_responsabilidade = db.Column(db.Float, nullable=True)
    empresa_nota_etica = db.Column(db.Float, nullable=True)
    empresa_atividades = db.Column(db.Text, nullable=True)
    emprsa_comentarios = db.Column(db.Text, nullable=True)
    empresa_media_notas = db.Column(db.Float, nullable=True)
    
    supervisor_nota_interesse = db.Column(db.Float, nullable=True)
    supervisor_nota_iniciativa = db.Column(db.Float, nullable=True)
    supervisor_nota_cooperacao = db.Column(db.Float, nullable=True)
    supervisor_nota_assiduidade_e_pontuabilidade = db.Column(db.Float, nullable=True)
    supervisor_nota_criatividade_e_engenhosidade = db.Column(db.Float, nullable=True)
    supervisor_nota_disciplina = db.Column(db.Float, nullable=True)
    supervisor_nota_sociabilidade = db.Column(db.Float, nullable=True)
    supervisor_nota_adaptabilidade = db.Column(db.Float, nullable=True)
    supervisor_nota_responsabilidade = db.Column(db.Float, nullable=True)
    supervisor_evolucao_tecnica = db.Column(db.Float, nullable=True)
    supervisor_nota_etica = db.Column(db.Float, nullable=True)
    supervisor_atividades = db.Column(db.Text, nullable=True)
    supervisor_comentarios = db.Column(db.Text, nullable=True)
    supervisor_media_notas = db.Column(db.Float, nullable=True)
    
    professor_nota_avaliacao = db.Column(db.Float, nullable=True)
    professor_avaliacao_comentarios = db.Column(db.Text, nullable=True)
    
    banca_nota_avaliacao_empresa = db.Column(db.Float, nullable=True)
    banca_nota_avaliacao_orientador = db.Column(db.Float, nullable=True)
    banca_nota_apresentacao_oral_1 = db.Column(db.Float, nullable=True)
    banca_nota_pratica_profissional_1 = db.Column(db.Float, nullable=True)
    banca_nota_relatorio_1 = db.Column(db.Float, nullable=True)
    banca_nota_apresentacao_oral_2 = db.Column(db.Float, nullable=True)
    banca_nota_pratica_profissional_2 = db.Column(db.Float, nullable=True)
    banca_nota_relatorio_2 = db.Column(db.Float, nullable=True)
    banca_avaliador_1 = db.Column(db.Text, nullable=True)
    banca_avaliador_2 = db.Column(db.Text, nullable=True)
    banca_autoavaliacao = db.Column(db.Float, nullable=True)
    banca_aprovado = db.Column(db.Boolean, nullable=True)
    banca_reprovado = db.Column(db.Boolean, nullable=True)
    banca_aprovado_com_ressalva = db.Column(db.Boolean, nullable=True)
    banca_relatorio_entrega = db.Column(db.Date, nullable=True)
    banca_refazer_apresentacao = db.Column(db.Date, nullable=True)
    banca_comentarios = db.Column(db.Text, nullable=True)
    
    aluno = db.relationship('Aluno', backref=db.backref('estagios', lazy=True))
    professor = db.relationship('Professor', backref=db.backref('estagios', lazy=True))
    supervisor = db.relationship('Supervisor', backref=db.backref('estagios', lazy=True))
    empresa = db.relationship('Empresa', backref=db.backref('estagios', lazy=True))
    
    def __repr__(self):
        return f'<Estagio {self.id} do Aluno {self.aluno_id}>'
