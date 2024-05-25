from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registrar')
