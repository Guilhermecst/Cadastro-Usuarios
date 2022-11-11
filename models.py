from cadastro import db


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(20), primary_key=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
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

    def __repr__(self):
        return '<Name %r>' % self.name
