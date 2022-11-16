from flask import render_template, request, redirect, session, flash, url_for
from app import app, db
from models import Usuarios, Agenda


# ------------------------------------------------------------------
# Read

@app.route('/usuarios')
def usuarios():
    usuarios = Usuarios.query.order_by(Usuarios.id)
    return render_template('usuarios.html', titulo='Usuários', usuarios=usuarios)


@app.route('/agendamentos')
def agendamentos():
    agendamentos = Agenda.query.order_by(Agenda.id_agendamento)
    return render_template('agendamentos.html', titulo='Agendamentos', agendamentos=agendamentos)


# ------------------------------------------------------------------
# Create

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo usuário')


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    data_nasc = request.form['data_nasc']
    genero = request.form['genero']
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

    Usuarios.adicionar_usuario(nome, sobrenome, data_nasc, genero, email, telefone,
                               cpf, cep, uf, cidade, rua, numero, complemento, bairro, nickname, senha)

    return redirect(url_for('login'))


@app.route('/agendar-horario', methods=['POST'])
def agendar_horario():
    servico = request.form['servico']
    data = request.form['data']
    hora = request.form['hora']
    nome_cliente = request.form['nome_cliente']
    email_cliente = request.form['email_cliente']
    telefone_cliente = request.form['telefone_cliente']

    Agenda.adicionar_agendamento(
        nome_cliente, servico, data, hora, email_cliente, telefone_cliente)

    flash('Agendamento efetuado com sucesso!')
    return redirect(url_for('agendamentos'))


# ------------------------------------------------------------------
# Update

@app.route('/editar/<int:id>')
def editar(id):
    if 'nickname' not in session or session['nickname'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    usuario = Usuarios.query.filter_by(id=id).first()
    if session['id'] != int(id):
        flash('Você não pode editar os dados de outro usuário')
        return redirect(url_for('usuarios'))
    return render_template('editar.html', titulo=f'Editar dados de {usuario.nome}', usuario=usuario)


@app.route('/editar-agendamento/<int:id_agendamento>')
def editar_agendamento(id_agendamento):
    if 'nickname' not in session or session['nickname'] == None:
        return redirect(url_for('login', proxima=url_for('editar_agendamento', id_agendamento=id_agendamento)))
    agendamento = Agenda.query.filter_by(id_agendamento=id_agendamento).first()
    return render_template('editar_agendamento.html', titulo=f'Editar agendamento de {agendamento.nome_cliente}', agendamento=agendamento)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    usuario = Usuarios.query.filter_by(
        nickname=request.form['nickname']).first()
    usuario.email = request.form['email']
    usuario.telefone = request.form['telefone']
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

    return redirect(url_for('usuarios'))


@app.route('/atualizar-agendamento', methods=['POST', ])
def atualizar_agendamento():
    pass


# ------------------------------------------------------------------
# Delete

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'nickname' not in session or session['nickname'] == None:
        return redirect(url_for('login'))

    if session['id'] != int(id):
        flash(session['id'])
        return redirect(url_for('usuarios'))
    Usuarios.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso!')
    return redirect(url_for('logout'))


@app.route('/deletar-agendamento/<int:id_agendamento>')
def deletar_agendamento(id_agendamento):
    if 'nickname' not in session or session['nickname'] == None:
        return redirect(url_for('login'))

    Agenda.query.filter_by(id_agendamento=id_agendamento).delete()
    db.session.commit()
    flash('Agendamento deletado com sucesso!')

    return redirect(url_for('agendamentos'))


# ------------------------------------------------------------------
# Login/Logout

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuarios.query.filter_by(
        nickname=request.form['nickname']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['id'] = usuario.id
            session['nickname'] = usuario.nickname
            session['nome'] = usuario.nome
            session['email'] = usuario.email
            session['telefone'] = usuario.telefone
            flash(usuario.nome + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['id'] = None
    session['nome'] = None
    session['nickname'] = None
    session['email'] = None
    session['telefone'] = None
    return redirect(url_for('login'))

# ------------------------------------------------------------------
# Outras


@app.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')


@app.route('/agenda')
def agenda():
    return render_template('agenda.html')


@app.route('/perfil')
def perfil():
    usuarios = Usuarios.query.order_by(Usuarios.id)
    return render_template('perfil.html', usuarios=usuarios)
