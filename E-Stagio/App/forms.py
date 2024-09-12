from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField, TextAreaField, BooleanField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
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
    empresa_nota_interesse = FloatField('Interesse', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_iniciativa = FloatField('Iniciativa', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_cooperacao = FloatField('Cooperação', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_assiduidade = FloatField('Assiduidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_pontualidade = FloatField('Pontualidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_disciplina = FloatField('Disciplina', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_sociabilidade = FloatField('Sociabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_adaptabilidade = FloatField('Adaptabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_responsabilidade = FloatField('Responsabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_nota_etica = FloatField('Ética', validators=[DataRequired(), NumberRange(min=0, max=10)])
    empresa_atividades = TextAreaField('Atividades', validators=[DataRequired()])
    emprsa_comentarios = TextAreaField('Comentários')
    submit = SubmitField('Salvar Avaliação')
    
class SupervisorAvaliacaoForm(FlaskForm):
    supervisor_nota_interesse = FloatField('Interesse', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_iniciativa = FloatField('Iniciativa', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_cooperacao = FloatField('Cooperação', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_assiduidade_e_pontualidade = FloatField('Assiduidade e Pontualidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_criatividade_e_engenhosidade = FloatField('Criatividade e Engenhosidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_disciplina = FloatField('Disciplina', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_sociabilidade = FloatField('Sociabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_adaptabilidade = FloatField('Adaptabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_responsabilidade = FloatField('Sendo de Responsabilidade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_evolucao_tecnica = FloatField('Evolução Técnica', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_nota_etica = FloatField('Evolução Técnica', validators=[DataRequired(), NumberRange(min=0, max=10)])
    supervisor_atividades = TextAreaField('Atividades', validators=[DataRequired()])
    supervisor_comentarios = TextAreaField('Comentários')
    submit = SubmitField('Salvar Avaliação')
    
class ProfessorAvaliacaoForm(FlaskForm):
    professor_nota_avaliacao = FloatField('Levando em conta os aspectos como interesse, iniciativa, comprometimento, prazos, e atividades desenvolvidas pleo estagiário(a) a nota de 0 a 10 é', validators=[DataRequired(), NumberRange(min=0, max=10)])
    professor_avaliacao_comentarios = TextAreaField('Comentários / Oberservações')
    submit = SubmitField('Salvar Avaliação')
    
class BancaAvaliacaoForm(FlaskForm):
    banca_nota_avaliacao_empresa = FloatField('Nota Avaliação Empresa', render_kw={'readonly': True})
    banca_nota_avaliacao_orientador = FloatField('Nota Avaliação Orientador', render_kw={'readonly': True})
    banca_autoavaliacao = FloatField('Autoavaliação', render_kw={'readonly': True})
    banca_nota_apresentacao_oral_1 = FloatField('Nota Apresentação Oral 1', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_nota_pratica_profissional_1 = FloatField('Nota Prática Profissional 1', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_nota_relatorio_1 = FloatField('Nota Relatório 1', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_nota_apresentacao_oral_2 = FloatField('Nota Apresentação Oral 2', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_nota_pratica_profissional_2 = FloatField('Nota Prática Profissional 2', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_nota_relatorio_2 = FloatField('Nota Relatório 2', validators=[DataRequired(), NumberRange(min=0, max=10)])
    banca_avaliador_1 = TextAreaField('Avaliador 1', validators=[DataRequired()])
    banca_avaliador_2 = TextAreaField('Avaliador 2', validators=[DataRequired()])
    banca_aprovado = BooleanField('Aprovado', validators=[Optional()])
    banca_reprovado = BooleanField('Reprovado', validators=[Optional()])
    banca_aprovado_com_ressalva = BooleanField('Aprovado com Ressalva', validators=[Optional()])
    banca_relatorio_entrega = DateField('Data de Entrega do Relatório', validators=[Optional()])
    banca_refazer_apresentacao = DateField('Data para Refazer Apresentação', validators=[Optional()])
    banca_comentarios = TextAreaField('Comentários', validators=[Optional()])
    
class EstagioFormAdd(FlaskForm):
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
    submit = SubmitField('Salvar Estágio')
    
class AutoAvaliacaoForm(FlaskForm):
    aluno_nota_rendimento = FloatField('Rendimento', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_facilidade_e_compreensao = FloatField('Facilidade e Compreensão', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_conhecimentos_tecnicos = FloatField('Conhecimentos Técnicos', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_organizacao_metodo_trabalho = FloatField('Organização e Método de Trabalho', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_iniciativa_independencia = FloatField('Iniciativa e Independência', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_disciplina = FloatField('Disciplina', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_sociabilidade_desempenho = FloatField('Sociabilidade e Desempenho', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_assiduidade = FloatField('Assiduidade', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_cooperecao = FloatField('Cooperação', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_nota_responsabilidade = FloatField('Responsabilidade', validators=[Optional(), NumberRange(min=0, max=10)])
    aluno_atividades = TextAreaField('Descreva as atividades realizadas', validators=[Optional()])
    aluno_comentarios = TextAreaField('Comentários', validators=[Optional()])

    # Campos de avaliação com valores 1 = sim, 2 = não, 3 = mais ou menos
    aluno_avaliacao_empresa_condicoes = IntegerField('A empresa ofereceu boas condições de trabalho?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_atendeu_expectativas = IntegerField('O estágio atendeu suas expectativas?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_contribui_formacao_profissional = IntegerField('O estágio contribuiu para sua formação profissional?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_recomendaria_para_outro = IntegerField('Recomendaria a empresa para outro aluno?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_curso_capacitou = IntegerField('O curso capacitou adequadamente para o estágio?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_orientador_acompanhou = IntegerField('O orientador acompanhou adequadamente?', validators=[Optional(), NumberRange(min=1, max=3)])
    aluno_avaliacao_supervisor_acompanhou = IntegerField('O supervisor acompanhou adequadamente?', validators=[Optional(), NumberRange(min=1, max=3)])

    submit = SubmitField('Salvar Autoavaliação')