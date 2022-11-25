import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='SuperAdmin&123'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `salao`;")

cursor.execute("CREATE DATABASE `salao`;")

cursor.execute("USE `salao`;")

# criando tabelas
TABLES = {}
TABLES['clientes'] = ('''
      CREATE TABLE `clientes` (
      `id` INT(5) NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(20) NOT NULL,
      `sobrenome` VARCHAR(50) NOT NULL,
      `data_nasc` VARCHAR(10) NOT NULL,
      `genero` VARCHAR(15) NOT NULL,
      `email` VARCHAR(100) NOT NULL,
      `telefone` VARCHAR(15) NOT NULL,
      `cpf` VARCHAR(14) NOT NULL,
      `cep` VARCHAR(9) NOT NULL,
      `uf` VARCHAR(2) NOT NULL,
      `cidade` VARCHAR(30) NOT NULL,
      `rua` VARCHAR(60) NOT NULL,
      `numero` VARCHAR(10) NOT NULL,
      `complemento` VARCHAR(15),
      `bairro` VARCHAR(30) NOT NULL,
      `nickname` VARCHAR(20) NOT NULL,
      `senha` VARCHAR(102) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['servicos'] = ('''
      CREATE TABLE `servicos` (
      `id_servico` INT(5) NOT NULL AUTO_INCREMENT,
      `nome_servico` VARCHAR(15) NOT NULL,
      `valor` VARCHAR(6) NOT NULL,
      PRIMARY KEY (`id_servico`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['agendamentos'] = ('''
      CREATE TABLE `agendamentos` (
      `id_agendamento` INT(5) NOT NULL AUTO_INCREMENT,
      `data` VARCHAR(10) NOT NULL,
      `servico` VARCHAR(15) NOT NULL,
      `hora` VARCHAR(5) NOT NULL,
      `nome_cliente` VARCHAR(20) NOT NULL,
      `email_cliente` VARCHAR(120) NOT NULL,
      `telefone_cliente` VARCHAR(15) NOT NULL,
      `id_cliente` INT(5) NOT NULL,
      `id_servico` INT(5) NOT NULL,
      PRIMARY KEY (`id_agendamento`),
      CONSTRAINT FK_id_cliente FOREIGN KEY (`id_cliente`) REFERENCES clientes(`id`),
      CONSTRAINT FK_id_servico FOREIGN KEY (`id_servico`) REFERENCES servicos(`id_servico`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')


# inserindo clientes
cliente_sql = 'INSERT INTO clientes (nome, sobrenome, data_nasc, genero, email, telefone, cpf, cep, uf, cidade, rua, numero, complemento, bairro, nickname, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
clientes = [
    ("Guilherme", "Costa Silva", "24/11/2001", "Masculino", "guilherme@gmail.com", "(11) 98765-4321", "123.456.789-10",
     "06160-265", "SP", "Osasco", "Rua Anastácia", "48", None, "Bandeiras", "guilherme",  "teste123"),
]
cursor.executemany(cliente_sql, clientes)

cursor.execute('select * from clientes')
print(' -------------  Usuários:  -------------')
for usuario in cursor.fetchall():
    print(usuario[15])

# inserindo servicos
servico_sql = 'INSERT INTO servicos (nome_servico, valor) VALUES (%s, %s)'
servicos = [
    ("Corte", "69,90"),
    ("Barba", "29,90"),
    ("Manicure", "49,90"),
    ("Pedicure", "59,90")
]
cursor.executemany(servico_sql, servicos)

cursor.execute('select * from servicos')
print(' -------------  Serviços:  -------------')
for servicos in cursor.fetchall():
    print(servicos[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
