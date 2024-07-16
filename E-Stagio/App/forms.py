from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')
    
class EmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=14, max=14)])
    qsa = StringField('QSA', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    nome_responsavel = StringField('Nome do Responsável', validators=[DataRequired()])
    email_responsavel = StringField('Email do Responsável', validators=[DataRequired(), Email()])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[DataRequired()])
    rg_responsavel = StringField('RG do Responsável', validators=[DataRequired()])
    cpf_responsavel = StringField('CPF do Responsável', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Registrar')
    
class SupervisorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    password = PasswordField('Senha', validators=[DataRequired()])
    formacao = StringField('Formação', validators=[DataRequired()])
    empresaId = SelectField('Empresa', coerce=int, validators=[DataRequired()])  # Changed to SelectField
    submit = SubmitField('Registrar')
    
class AlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    matricula = StringField('Número de Matricula', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    celular = StringField('Telefone', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    rg = StringField('RG', validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Senha', validators=[DataRequired()])
    dob = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Registrar')