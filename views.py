from flask import render_template, request, redirect, session, flash, url_for
from cadastro import app, db
from models import Usuarios


@app.route('/')
def index():
    lista = Usuarios.query.order_by(Usuarios.id)
    return render_template('lista.html', titulo='Usuários', usuarios=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo usuário')

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    data_nasc = request.form['data_nasc']
    email = request.form['email']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    cep = request.form['cep']
    uf = request.form['uf']
    cidade = request.form['cidade']
    rua = request.form['rua']
    numero = request.form['numero']
    complemento = request.form['complemento']
    bairro = request.form['bairro']
    # Dados de login
    nickname = request.form['nickname']
    senha = request.form['senha']

    usuario = Usuarios.query.filter_by(nickname=nickname).first()

    if usuario:
        flash('Usuário já existe')
        return redirect(url_for('criar'))

    novo_usuario = Usuarios(nome=nome, sobrenome=sobrenome, data_nasc=data_nasc,
                            email=email, telefone=telefone,
                            cpf=cpf, cep=cep, uf=uf, cidade=cidade,
                            rua=rua, numero=numero, complemento=complemento,
                            bairro=bairro, nickname=nickname, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    usuario = Usuarios.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editar dados de usuário', usuario=usuario)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    usuario = Usuarios.query.filter_by(nickname=request.form['nickname']).first()
    usuario.nome = request.form['nome']
    usuario.sobrenome = request.form['sobrenome']
    usuario.data_nasc = request.form['data_nasc']
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
    usuario.cpf = request.form['cpf']
    usuario.cep = request.form['cep']
    usuario.uf = request.form['uf']
    usuario.cidade = request.form['cidade']
    usuario.rua = request.form['rua']
    usuario.numero = request.form['numero']
    usuario.complemento = request.form['complemento']
    usuario.bairro = request.form['bairro']
    # Dados de login
    usuario.nickname = request.form['nickname']
    usuario.senha = request.form['senha']

    db.session.add(usuario)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['nickname']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo='Contato')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))