SECRET_KEY = 'secretKey'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='SuperAdmin&123',
        servidor='localhost',
        database='salao'
    )
