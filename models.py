from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(id):
    return Usuarios.query.filter_by(id=id).first()


class Usuarios(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    data_nasc = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(15), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(30), nullable=False)
    rua = db.Column(db.String(60), nullable=False)
    numero = db.Column(db.String(5), nullable=False)
    complemento = db.Column(db.String(15))
    bairro = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(20), nullable=False, unique=True)
    senha = db.Column(db.String(50), nullable=False)
    agendamento = db.relationship('Agendamentos', backref='id', lazy=True)

    def adicionar_usuario(nome, sobrenome, data_nasc, genero, email, telefone, cpf, cep, uf, cidade, rua, numero, complemento, bairro, nickname, senha):
        usuario = Usuarios(nome=nome, sobrenome=sobrenome, data_nasc=data_nasc, genero=genero,
                           email=email, telefone=telefone,
                           cpf=cpf, cep=cep, uf=uf, cidade=cidade,
                           rua=rua, numero=numero, complemento=complemento,
                           bairro=bairro, nickname=nickname, senha=generate_password_hash(senha))
        db.session.add(usuario)
        db.session.commit()

    def verificar_senha(self, pwd):
        return check_password_hash(self.senha, pwd)


class Servicos(db.Model, UserMixin):
    __tablename__ = 'servicos'
    id_servico = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    nome_servico = db.Column(db.String(15), nullable=False)

    def adicionar_servico(nome_servico):
        servico = Servicos(nome_servico=nome_servico)
        db.session.add(servico)
        db.session.commit()

    def __repr__(self):
        return '<Name %r>' % self.name


class Agendamentos(db.Model, UserMixin):
    __tablename__ = 'agendamentos'
    id_agendamento = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(20), nullable=False)
    servico = db.Column(db.String(15), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefone_cliente = db.Column(db.String(15), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuarios.id'),
                           nullable=False)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id_servico'),
                           nullable=False)

    def adicionar_agendamento(nome_cliente, servico, data, hora, email_cliente, telefone_cliente, id_cliente, id_servico):
        agendamento = Agendamentos(nome_cliente=nome_cliente, servico=servico, data=data,
                                   hora=hora, email_cliente=email_cliente, telefone_cliente=telefone_cliente, id_cliente=id_cliente, id_servico=id_servico)
        db.session.add(agendamento)
        db.session.commit()

    def __repr__(self):
        return '<Name %r>' % self.name


class Contato:
    def __init__(self, nome, email, telefone, assunto, mensagem):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.assunto = assunto
        self.mensagem = mensagem
