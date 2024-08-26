from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField, TextAreaField, BooleanField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from app.models import StatusEstagio

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
class ProfessorFormEdit(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')
    
class EmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=18)])
    qsa = StringField('QSA', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    nome_responsavel = StringField('Nome do Responsável', validators=[DataRequired()])
    email_responsavel = StringField('Email do Responsável', validators=[DataRequired(), Email()])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[DataRequired()])
    rg_responsavel = StringField('RG do Responsável', validators=[DataRequired()])
    cpf_responsavel = StringField('CPF do Responsável', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Registrar')

class EmpresaEditForm(FlaskForm):
    nome_empresa = StringField('Nome da Empresa', validators=[DataRequired()])
    email_empresa = StringField('Email da Empresa', validators=[DataRequired(), Email()])
    telefone_empresa = StringField('Telefone da Empresa', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=18)])
    qsa = StringField('QSA', validators=[DataRequired()])
    nome_responsavel = StringField('Nome do Responsável', validators=[DataRequired()])
    email_responsavel = StringField('Email do Responsável', validators=[DataRequired(), Email()])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[DataRequired()])
    rg_responsavel = StringField('RG do Responsável', validators=[DataRequired()])
    cpf_responsavel = StringField('CPF do Responsável', validators=[DataRequired(), Length(min=11, max=14)])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')

class SupervisorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    password = PasswordField('Senha', validators=[DataRequired()])
    formacao = StringField('Formação', validators=[DataRequired()])
    empresaId = SelectField('Empresa', coerce=int, validators=[DataRequired()])  # Changed to SelectField
    submit = SubmitField('Registrar')
    
class SupervisorEditForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    formacao = StringField('Formação', validators=[DataRequired()])
    empresaId = SelectField('Empresa', coerce=int, validators=[DataRequired()])  # Changed to SelectField
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')

class AlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    matricula = StringField('Número de Matricula', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    celular = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    rg = StringField('RG', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Senha', validators=[DataRequired()])
    dob = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
class AlunoEditForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    matricula = StringField('Número de Matricula', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    celular = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=14)])
    rg = StringField('RG', validators=[DataRequired(), Length(min=3, max=15)])
    dob = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired()])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')
    
class EstagioForm(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int, validators=[DataRequired()])
    professor_id = SelectField('Professor', coerce=int, validators=[DataRequired()])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[DataRequired()])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired()])
    modalidade = StringField('Modalidade', validators=[DataRequired()])
    carga_horaria = IntegerField('Carga Horária', validators=[DataRequired()])
    atividades = TextAreaField('Atividades', validators=[DataRequired()])
    setor = StringField('Setor', validators=[DataRequired()])
    remuneracao = BooleanField('Remuneração')
    valor_remuneracao = FloatField('Valor da Remuneração', default=0.0)
    horario_estagio = StringField('Horário do Estágio', validators=[DataRequired()])
    data_inicio = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    data_conclusao = DateField('Data de Conclusão', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', coerce=str, choices=[(choice.name, choice.value.replace('_', ' ').title()) for choice in StatusEstagio], validators=[DataRequired()])
    submit = SubmitField('Salvar Estágio')
    
class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Registrar')
    
class EmpresaAvaliacaoForm(FlaskForm):
    empresa_nota_interesse = FloatField('Interesse', validators=[NumberRange(min=0, max=10)])
    empresa_nota_iniciativa = FloatField('Iniciativa', validators=[NumberRange(min=0, max=10)])
    empresa_nota_cooperacao = FloatField('Cooperação', validators=[NumberRange(min=0, max=10)])
    empresa_nota_assiduidade = FloatField('Assiduidade', validators=[NumberRange(min=0, max=10)])
    empresa_nota_pontualidade = FloatField('Pontualidade', validators=[NumberRange(min=0, max=10)])
    empresa_nota_disciplina = FloatField('Disciplina', validators=[NumberRange(min=0, max=10)])
    empresa_nota_sociabilidade = FloatField('Sociabilidade', validators=[NumberRange(min=0, max=10)])
    empresa_nota_adaptabilidade = FloatField('Adaptabilidade', validators=[NumberRange(min=0, max=10)])
    empresa_nota_responsabilidade = FloatField('Responsabilidade', validators=[NumberRange(min=0, max=10)])
    empresa_nota_etica = FloatField('Ética', validators=[NumberRange(min=0, max=10)])
    empresa_atividades = TextAreaField('Atividades', validators=[DataRequired()])
    emprsa_comentarios = TextAreaField('Comentários')
    submit = SubmitField('Salvar Avaliação')
    
class EmpresaAvaliacaoForm(FlaskForm):
    supervisor_nota= FloatField('Nota', validators=[NumberRange(min=0, max=10)])
    supervisor_comentarios = TextAreaField('Comentários ou Observações')
    estagiario_name = TextAreaField('Aluno')
    estagiario_concedente = TextAreaField('Concedente')
    
    submit = SubmitField('Salvar Avaliação')