from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from app import app, db, mail
from models import Clientes, Servicos, Agendamentos, Contato


# ------------------------------------------------------------------
# Read

@app.route('/clientes')
def clientes():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('clientes')))
    clientes = Clientes.query.order_by(Clientes.id)
    return render_template('clientes.html', titulo='Clientes', clientes=clientes)


@app.route('/agendamentos')
def agendamentos():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('agendamentos')))
    agendamentos = Agendamentos.query.order_by(Agendamentos.id_agendamento)
    return render_template('agendamentos.html', titulo='Agendamentos', agendamentos=agendamentos)


@app.route('/servicos')
def servicos():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('servicos')))
    servicos = Servicos.query.order_by(Servicos.id_servico)
    return render_template('servicos.html', titulo='Serviços', servicos=servicos)


@app.route('/meus-agendamentos')
def meus_agendamentos():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('meus_agendamentos')))
    meus_agendamentos = Agendamentos.query.order_by(Agendamentos.id_cliente)
    return render_template('meus_agendamentos.html', titulo='Meus agendamentos', meus_agendamentos=meus_agendamentos)


@app.route('/servicos-e-precos')
def servicos_precos():
    servicos = Servicos.query.order_by(Servicos.id_servico)
    return render_template('servicos_precos.html', titulo='Preços R$', servicos=servicos)


# ------------------------------------------------------------------
# Create

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo usuário')


@app.route('/agenda')
def agenda():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('agenda')))
    servicos = Servicos.query.order_by(Servicos.id_servico)
    return render_template('agenda.html', servicos=servicos)


@app.route('/novo-servico')
def novo_servico():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('novo_servico')))
    return render_template('novo_servico.html', titulo='Adicionar serviço')


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

    cliente = Clientes.query.filter_by(nickname=nickname).first()

    if cliente:
        flash('Usuário já existe')
        return redirect(url_for('novo'))

    Clientes.adicionar_cliente(nome, sobrenome, data_nasc, genero, email, telefone,
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
    id_cliente = request.form['id_cliente']

    nome_servico = Servicos.query.filter_by(
        nome_servico=request.form['servico']).first()

    id_servico = nome_servico.id_servico

    Agendamentos.adicionar_agendamento(
        nome_cliente, servico, data, hora, email_cliente, telefone_cliente, id_cliente, id_servico)

    msg = Message(
        subject=f'Confirmação de agendamento',
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[email_cliente],
        body=f'''
            
Este é um e-mail automático de confirmação de agendamento, por favor não responda.

Agendamento de {servico} marcado para {data} às {hora}.


            '''
    )
    mail.send(msg)

    flash('Agendamento efetuado com sucesso!')
    return redirect(url_for('meus_agendamentos'))


@app.route('/criar-servico', methods=['POST'])
def criar_servico():
    nome_servico = request.form['nome_servico']
    valor = request.form['valor']

    servico = Servicos.query.filter_by(nome_servico=nome_servico).first()

    if servico:
        flash('Serviço já existe')
        return redirect(url_for('novo_servico'))

    Servicos.adicionar_servico(nome_servico, valor)

    flash('Serviço adicionado com sucesso!')
    return redirect(url_for('novo_servico'))

# ------------------------------------------------------------------
# Update


@app.route('/editar/<int:id>')
def editar(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    cliente = Clientes.query.filter_by(id=id).first()
    if current_user.id != int(id):
        flash('Você não pode editar os dados de outro usuário')
        return redirect(url_for('clientes'))
    return render_template('editar.html', titulo=f'Editar dados de {cliente.nome}', cliente=cliente)


@app.route('/editar-agendamento/<int:id_agendamento>')
def editar_agendamento(id_agendamento):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('editar_agendamento', id_agendamento=id_agendamento)))
    agendamento = Agendamentos.query.filter_by(
        id_agendamento=id_agendamento).first()
    servicos = Servicos.query.order_by(Servicos.id_servico)
    if current_user.id != int(agendamento.id_cliente):
        flash('Você não pode editar o agendamento de outro usuário')
        return redirect(url_for('agendamentos'))
    return render_template('editar_agendamento.html', titulo=f'Editar agendamento de {agendamento.nome_cliente}', agendamento=agendamento, servicos=servicos)


@app.route('/editar-servico/<int:id_servico>')
def editar_servico(id_servico):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('editar_servico', id_servico=id_servico)))
    servico = Servicos.query.filter_by(
        id_servico=id_servico).first()
    return render_template('editar_servico.html', titulo=f'Editar serviço', servico=servico)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    cliente = Clientes.query.filter_by(
        id=request.form['id']).first()
    cliente.email = request.form['email']
    cliente.telefone = request.form['telefone']
    cliente.cep = request.form['cep']
    cliente.uf = request.form['uf']
    cliente.cidade = request.form['cidade']
    cliente.rua = request.form['rua']
    cliente.numero = request.form['numero']
    cliente.complemento = request.form['complemento']
    cliente.bairro = request.form['bairro']

    db.session.add(cliente)
    db.session.commit()

    flash(f'Dados de {cliente.nome} editados com sucesso!')
    return redirect(url_for('perfil'))


@app.route('/atualizar-agendamento', methods=['POST', ])
def atualizar_agendamento():
    agendamento = Agendamentos.query.filter_by(
        id_agendamento=request.form['id_agendamento']).first()
    agendamento.servico = request.form['servico']
    agendamento.data = request.form['data']
    agendamento.hora = request.form['hora']
    agendamento.nome_cliente = request.form['nome_cliente']
    agendamento.email_cliente = request.form['email_cliente']
    agendamento.telefone_cliente = request.form['telefone_cliente']
    agendamento.id_cliente = request.form['id_cliente']

    nome_servico = Servicos.query.filter_by(
        nome_servico=request.form['servico']).first()

    id_servico = nome_servico.id_servico

    agendamento.id_servico = id_servico

    db.session.add(agendamento)
    db.session.commit()

    msg = Message(
        subject=f'Alteração no agendamento',
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[agendamento.email_cliente],
        body=f'''
            
Este é um e-mail automático de alteração no agendamento, por favor não responda.

Agendamento alterado para {agendamento.servico} remarcado para {agendamento.data} às {agendamento.hora}.


            '''
    )
    mail.send(msg)

    flash(f'Agendamento de {agendamento.nome_cliente} editado com sucesso!')
    return redirect(url_for('meus_agendamentos'))


@app.route('/atualizar-servico', methods=['POST', ])
def atualizar_servico():
    servico = Servicos.query.filter_by(
        id_servico=request.form['id_servico']).first()
    servico.nome_servico = request.form['nome_servico']
    servico.valor = request.form['valor']

    db.session.add(servico)
    db.session.commit()

    flash(f'Serviço editado com sucesso!')
    return redirect(url_for('servicos'))


@app.route('/alterar-senha/<string:nickname>')
def alterar_senha(nickname):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('alterar_senha', nickname=nickname)))
    cliente = Clientes.query.filter_by(
        nickname=nickname).first()
    if current_user.id != int(cliente.id):
        flash('Você não pode redefinir a senha de outro usuário')
    return render_template('alterar_senha.html', titulo=f'Alterar senha', nickname=nickname)


@app.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    cliente = Clientes.query.filter_by(
        nickname=request.form['nickname']).first()

    senha_atual = request.form['senha_atual']
    senha = request.form['senha']

    if cliente.verificar_senha(senha_atual):
        cliente.senha = generate_password_hash(senha)
        db.session.add(cliente)
        db.session.commit()

        flash(f'Senha alterada')
        return redirect(url_for('agenda'))
    else:
        flash(f'Senha incorreta')
        return redirect(url_for('alterar_senha', nickname=current_user.nickname))


# ------------------------------------------------------------------
# Delete

@app.route('/deletar/<int:id>')
def deletar(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('deletar'), id=id))
    if current_user.id != int(id):
        flash('Você não pode deletar os dados de outro usuário')
        return redirect(url_for('clientes'))
    Agendamentos.query.filter_by(id_cliente=id).delete()
    Clientes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário deletado com sucesso!')
    return redirect(url_for('logout'))


@app.route('/deletar-agendamento/<int:id_agendamento>')
def deletar_agendamento(id_agendamento):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('deletar-agendamento'), id_agendamento=id_agendamento))
    agendamento = Agendamentos.query.filter_by(
        id_agendamento=id_agendamento).first()
    if current_user.id != int(agendamento.id_cliente):
        flash('Você não pode deletar o agendamento de outro usuário')
        return redirect(url_for('agendamentos'))
    Agendamentos.query.filter_by(id_agendamento=id_agendamento).delete()
    db.session.commit()
    flash('Agendamento deletado com sucesso!')

    return redirect(url_for('meus_agendamentos'))


@app.route('/deletar-servico/<int:id_servico>')
def deletar_servico(id_servico):
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('deletar-servico'), id_servico=id_servico))
    servico = Servicos.query.filter_by(
        id_servico=id_servico).first()
    Servicos.query.filter_by(id_servico=id_servico).delete()
    db.session.commit()
    flash('Serviço deletado com sucesso!')

    return redirect(url_for('servicos'))


# ------------------------------------------------------------------
# Login/Logout

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        senha = request.form['senha']

        cliente = Clientes.query.filter_by(nickname=nickname).first()

        if not cliente or not cliente.verificar_senha(senha):
            flash('Usuário ou senha inválidos')
            return redirect(url_for('login'))

        login_user(cliente)

        return redirect(url_for('agenda'))
    return render_template('login.html', titulo='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# ------------------------------------------------------------------
# Outras


@app.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')


@app.route('/perfil')
def perfil():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('perfil')))
    clientes = Clientes.query.order_by(Clientes.id)
    return render_template('perfil.html', clientes=clientes)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('contato')))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        form_contato = Contato(
            nome=nome, email=email, telefone=telefone, assunto=assunto, mensagem=mensagem)
        msg = Message(
            subject=f'{form_contato.assunto}',
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[app.config.get("MAIL_USERNAME")],
            body=f'''
            
{form_contato.nome} te enviou a seguinte mensagem:

{form_contato.mensagem}

Dados para contato:
Nome: {form_contato.nome}
E-mail: {form_contato.email}
Telefone: {form_contato.telefone}


            '''
        )
        mail.send(msg)
        flash('E-mail enviado com sucesso!')
        return redirect(url_for('contato'))
    return render_template('contato.html', titulo='Contato')


@app.route('/configuracoes')
def configuracoes():
    if not current_user.is_authenticated:
        return redirect(url_for('login', proxima=url_for('configuracoes')))
    return render_template('configuracoes.html', titulo='Configurações')
