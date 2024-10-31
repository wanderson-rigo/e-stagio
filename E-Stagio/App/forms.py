from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField, TextAreaField, BooleanField, FloatField, HiddenField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
from app.models import StatusEstagio

class ProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    password = PasswordField('Senha', validators=[DataRequired(message='Este campo é obrigatório.')])
    submit = SubmitField('Registrar')
    
class ProfessorFormEdit(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')
    
class EmpresaForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone = StringField('Telefone', validators=[DataRequired(message='Este campo é obrigatório.')])
    cnpj = StringField('CNPJ', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=14, max=18, message='O CNPJ deve ter entre 14 e 18 caracteres.')])
    qsa = StringField('QSA', validators=[DataRequired(message='Este campo é obrigatório.')])
    password = PasswordField('Senha', validators=[DataRequired(message='Este campo é obrigatório.')])
    nome_responsavel = StringField('Nome do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    email_responsavel = StringField('Email do Responsável', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    rg_responsavel = StringField('RG do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf_responsavel = StringField('CPF do Responsável', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=11, message='O CPF deve ter 11 caracteres.')])
    submit = SubmitField('Registrar')

class EmpresaEditForm(FlaskForm):
    nome_empresa = StringField('Nome da Empresa', validators=[DataRequired(message='Este campo é obrigatório.')])
    email_empresa = StringField('Email da Empresa', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone_empresa = StringField('Telefone da Empresa', validators=[DataRequired(message='Este campo é obrigatório.')])
    cnpj = StringField('CNPJ', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=14, max=18, message='O CNPJ deve ter entre 14 e 18 caracteres.')])
    qsa = StringField('QSA', validators=[DataRequired(message='Este campo é obrigatório.')])
    nome_responsavel = StringField('Nome do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    email_responsavel = StringField('Email do Responsável', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    rg_responsavel = StringField('RG do Responsável', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf_responsavel = StringField('CPF do Responsável', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')

class SupervisorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone = StringField('Telefone', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    password = PasswordField('Senha', validators=[DataRequired(message='Este campo é obrigatório.')])
    formacao = StringField('Formação', validators=[DataRequired(message='Este campo é obrigatório.')])
    empresaId = SelectField('Empresa', coerce=int, validators=[DataRequired(message='Este campo é obrigatório.')])
    submit = SubmitField('Registrar')
    
class SupervisorEditForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    telefone = StringField('Telefone', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    formacao = StringField('Formação', validators=[DataRequired(message='Este campo é obrigatório.')])
    empresaId = SelectField('Empresa', coerce=int, validators=[DataRequired(message='Este campo é obrigatório.')])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')

class AlunoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    matricula = StringField('Número de Matrícula', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    celular = StringField('Telefone', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    rg = StringField('RG', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=3, max=15, message='O RG deve ter entre 3 e 15 caracteres.')])
    password = PasswordField('Senha', validators=[DataRequired(message='Este campo é obrigatório.')])
    dob = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    submit = SubmitField('Registrar')
    
class AlunoEditForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message='Este campo é obrigatório.')])
    matricula = StringField('Número de Matrícula', validators=[DataRequired(message='Este campo é obrigatório.')])
    email = StringField('Email', validators=[DataRequired(message='Este campo é obrigatório.'), Email(message='Por favor, insira um endereço de email válido.')])
    celular = StringField('Telefone', validators=[DataRequired(message='Este campo é obrigatório.')])
    cpf = StringField('CPF', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=11, max=14, message='O CPF deve ter entre 11 e 14 caracteres.')])
    rg = StringField('RG', validators=[DataRequired(message='Este campo é obrigatório.'), Length(min=3, max=15, message='O RG deve ter entre 3 e 15 caracteres.')])
    dob = DateField("Data de Nascimento", format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Editar')
    
class EstagioForm(FlaskForm):
    aluno_id = SelectField('Aluno', coerce=int, validators=[DataRequired(message='Selecione um aluno.')])
    professor_id = SelectField('Professor', coerce=int, validators=[DataRequired(message='Selecione um professor.')])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[DataRequired(message='Selecione um supervisor.')])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired(message='Selecione uma empresa.')])
    modalidade = StringField('Modalidade', validators=[DataRequired(message='Este campo é obrigatório.')])
    carga_horaria = IntegerField('Carga Horária', validators=[DataRequired(message='Este campo é obrigatório.')])
    atividades = TextAreaField('Atividades', validators=[DataRequired(message='Este campo é obrigatório.')])
    setor = StringField('Setor', validators=[DataRequired(message='Este campo é obrigatório.')])
    remuneracao = BooleanField('Remuneração')
    valor_remuneracao = FloatField('Valor da Remuneração', default=0.0)
    horario_estagio = StringField('Horário do Estágio', validators=[DataRequired(message='Este campo é obrigatório.')])
    data_inicio = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    data_conclusao = DateField('Data de Conclusão', format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    status = SelectField('Status', coerce=str, choices=[(choice.name, choice.value.replace('_', ' ').title()) for choice in StatusEstagio], validators=[DataRequired(message='Selecione um status.')])
    submit = SubmitField('Salvar Estágio')
    
class AdminForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        Email(message='Por favor, insira um endereço de email válido.')
    ])
    password = PasswordField('Senha', validators=[DataRequired(message='Este campo é obrigatório.')])
    ativo = BooleanField('Ativo')
    submit = SubmitField('Registrar')

class EmpresaAvaliacaoForm(FlaskForm):
    empresa_nota_interesse = FloatField('Interesse', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_iniciativa = FloatField('Iniciativa', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_cooperacao = FloatField('Cooperação', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_assiduidade = FloatField('Assiduidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_pontualidade = FloatField('Pontualidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_disciplina = FloatField('Disciplina', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_sociabilidade = FloatField('Sociabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_adaptabilidade = FloatField('Adaptabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_responsabilidade = FloatField('Responsabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_nota_etica = FloatField('Ética', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    empresa_atividades = TextAreaField('Atividades', validators=[DataRequired(message='Este campo é obrigatório.')])
    emprsa_comentarios = TextAreaField('Comentários')
    submit = SubmitField('Salvar Avaliação')
    
class SupervisorAvaliacaoForm(FlaskForm):
    supervisor_nota_interesse = FloatField('Interesse', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_iniciativa = FloatField('Iniciativa', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_cooperacao = FloatField('Cooperação', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_assiduidade_e_pontuabilidade = FloatField('Assiduidade e Pontualidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_criatividade_e_engenhosidade = FloatField('Criatividade e Engenhosidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_disciplina = FloatField('Disciplina', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_sociabilidade = FloatField('Sociabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_adaptabilidade = FloatField('Adaptabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_responsabilidade = FloatField('Responsabilidade', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_evolucao_tecnica = FloatField('Evolução Técnica', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_nota_etica = FloatField('Ética', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    supervisor_atividades = TextAreaField('Atividades', validators=[DataRequired(message='Este campo é obrigatório.')])
    supervisor_comentarios = TextAreaField('Comentários')
    submit = SubmitField('Salvar Avaliação')
    
class ProfessorAvaliacaoForm(FlaskForm):
    professor_nota_avaliacao = FloatField('Levando em conta os aspectos como interesse, iniciativa, comprometimento, prazos, e atividades desenvolvidas pelo estagiário(a), a nota de 0 a 10 é:', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    professor_avaliacao_comentarios = TextAreaField('Comentários / Observações')
    submit = SubmitField('Salvar Avaliação')

class BancaAvaliacaoForm(FlaskForm):
    banca_nota_avaliacao_empresa = FloatField('Nota Avaliação Empresa', validators=[Optional()], render_kw={'readonly': True})
    banca_autoavaliacao = FloatField('Autoavaliação', validators=[Optional()], render_kw={'readonly': True})
    banca_nota_avaliacao_orientador = FloatField('Nota Avaliação Orientador', render_kw={'readonly': True})
    banca_nota_apresentacao_oral_1 = FloatField('Nota Apresentação Oral 1', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_pratica_profissional_1 = FloatField('Nota Prática Profissional 1', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_relatorio_1 = FloatField('Nota Relatório 1', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_apresentacao_oral_2 = FloatField('Nota Apresentação Oral 2', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_pratica_profissional_2 = FloatField('Nota Prática Profissional 2', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_relatorio_2 = FloatField('Nota Relatório 2', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_apresentacao_oral_supervisor = FloatField('Nota Apresentação Oral Supervisor', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_pratica_profissional_supervisor = FloatField('Nota Prática Profissional Supervisor', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_nota_relatorio_supervisor = FloatField('Nota Relatório Supervisor', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')
    ])
    banca_avaliador_1 = TextAreaField('Avaliador 1', validators=[DataRequired(message='Este campo é obrigatório.')])
    banca_avaliador_2 = TextAreaField('Avaliador 2', validators=[DataRequired(message='Este campo é obrigatório.')])
    banca_aprovado = BooleanField('Aprovado', validators=[Optional()])
    banca_reprovado = BooleanField('Reprovado', validators=[Optional()])
    banca_aprovado_com_ressalva = BooleanField('Aprovado com Ressalva', validators=[Optional()])
    banca_relatorio_entrega = DateField('Data de Entrega do Relatório', validators=[Optional()])
    banca_refazer_apresentacao = DateField('Data para Refazer Apresentação', validators=[Optional()])
    banca_comentarios = TextAreaField('Comentários', validators=[Optional()])
    
class EstagioFormAdd(FlaskForm):
    professor_id = SelectField('Professor', coerce=int, validators=[DataRequired(message='Selecione um professor.')])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[DataRequired(message='Selecione um supervisor.')])
    empresa_id = SelectField('Empresa', coerce=int, validators=[DataRequired(message='Selecione uma empresa.')])
    modalidade = StringField('Modalidade', validators=[DataRequired(message='Este campo é obrigatório.')])
    carga_horaria = IntegerField('Carga Horária', validators=[DataRequired(message='Este campo é obrigatório.')])
    atividades = TextAreaField('Atividades', validators=[DataRequired(message='Este campo é obrigatório.')])
    setor = StringField('Setor', validators=[DataRequired(message='Este campo é obrigatório.')])
    remuneracao = BooleanField('Remuneração')
    valor_remuneracao = FloatField('Valor da Remuneração', default=0.0)
    horario_estagio = StringField('Horário do Estágio', validators=[DataRequired(message='Este campo é obrigatório.')])
    data_inicio = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    data_conclusao = DateField('Data de Conclusão', format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    estagio_id = HiddenField('ID do Estágio')
    submit = SubmitField('Salvar Estágio')

class AutoAvaliacaoForm(FlaskForm):
    aluno_nota_rendimento = FloatField('Rendimento', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_facilidade_e_compreensao = FloatField('Facilidade e Compreensão', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_conhecimentos_tecnicos = FloatField('Conhecimentos Técnicos', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_organizacao_metodo_trabalho = FloatField('Organização e Método de Trabalho', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_iniciativa_independencia = FloatField('Iniciativa e Independência', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_disciplina = FloatField('Disciplina', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_sociabilidade_desempenho = FloatField('Sociabilidade e Desempenho', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_assiduidade = FloatField('Assiduidade', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_cooperecao = FloatField('Cooperação', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_nota_responsabilidade = FloatField('Responsabilidade', validators=[Optional(), NumberRange(min=0, max=10, message='A nota deve estar entre 0 e 10.')])
    aluno_atividades = TextAreaField('Descreva as atividades realizadas', validators=[Optional()])
    aluno_comentarios = TextAreaField('Comentários', validators=[Optional()])

    # Campos de avaliação com valores 1 = sim, 2 = não, 3 = mais ou menos
    aluno_avaliacao_empresa_condicoes = IntegerField('A empresa ofereceu boas condições de trabalho? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_atendeu_expectativas = IntegerField('O estágio atendeu suas expectativas? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_contribui_formacao_profissional = IntegerField('O estágio contribuiu para sua formação profissional? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_recomendaria_para_outro = IntegerField('Recomendaria a empresa para outro aluno? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_curso_capacitou = IntegerField('O curso capacitou adequadamente para o estágio? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_orientador_acompanhou = IntegerField('O orientador acompanhou adequadamente? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])
    aluno_avaliacao_supervisor_acompanhou = IntegerField('O supervisor acompanhou adequadamente? 1 - SIM, 2 - NÃO, 3 - Mais ou menos.', validators=[
        Optional(), NumberRange(min=1, max=3, message='O valor deve ser 1, 2 ou 3.')
    ])

    submit = SubmitField('Salvar Autoavaliação')

class AtividadesEstagioForm(FlaskForm):
    descricao = StringField('Descrição', validators=[
        DataRequired(message='Este campo é obrigatório.'),
        Length(max=255, message='A descrição deve ter no máximo 255 caracteres.')
    ])
    data = DateField('Data', format='%Y-%m-%d', validators=[DataRequired(message='Este campo é obrigatório.')])
    horario_entrada = TimeField('Horário de Entrada', validators=[DataRequired(message='Este campo é obrigatório.')])
    horario_saida = TimeField('Horário de Saída', validators=[DataRequired(message='Este campo é obrigatório.')])
    horas_totais = FloatField('Horas Totais', validators=[Optional(), NumberRange(min=0, message='O valor deve ser maior ou igual a 0.')])
    estagio_id = IntegerField('ID do Estágio', validators=[DataRequired(message='Este campo é obrigatório.')])
    submit = SubmitField('Registrar Atividade')