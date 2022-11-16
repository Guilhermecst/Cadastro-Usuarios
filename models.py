from app import db


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(20), primary_key=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    data_nasc = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    cep = db.Column(db.String(9), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    cidade = db.Column(db.String(30), nullable=False)
    rua = db.Column(db.String(60), nullable=False)
    numero = db.Column(db.String(5), nullable=False)
    complemento = db.Column(db.String(15))
    bairro = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    def adicionar_usuario(nome, sobrenome, data_nasc, genero, email, telefone, cpf, cep, uf, cidade, rua, numero, complemento, bairro, nickname, senha):
        usuario = Usuarios(nome=nome, sobrenome=sobrenome, data_nasc=data_nasc, genero=genero,
                             email=email, telefone=telefone,
                             cpf=cpf, cep=cep, uf=uf, cidade=cidade,
                             rua=rua, numero=numero, complemento=complemento,
                             bairro=bairro, nickname=nickname, senha=senha)
        db.session.add(usuario)
        db.session.commit()


class Agenda(db.Model):
    id_agendamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(20), nullable=False)
    servico = db.Column(db.String(15), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefone_cliente = db.Column(db.String(15), nullable=False)

    def adicionar_agendamento(nome_cliente, servico, data, hora, email_cliente, telefone_cliente):
        agendamento = Agenda(nome_cliente=nome_cliente, servico=servico, data=data,
                             hora=hora, email_cliente=email_cliente, telefone_cliente=telefone_cliente)
        db.session.add(agendamento)
        db.session.commit()

    def __repr__(self):
        return '<Name %r>' % self.name
