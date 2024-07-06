from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

application.config['SECRET_KEY'] = 'NFDBFNHBS##mnjn8*'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyFirstBloggBACK-END.db'

db = SQLAlchemy(application)
db:SQLAlchemy


class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer,db.ForeignKey('autor.id_autor'))


class Autor(db.Model):
    __tablename__ = 'autor'
    id_autor = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String)
    cpf = db.Column(db.Integer)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')


def inicializar_banco():
    with application.app_context():
        db.drop_all()
        db.create_all()
        autor = Autor(nome='MoisesSouza',cpf=99999999,email='randomdude666123@gmail.com',senha='Mn190887svb¨¨¨$%$',admin=True)
        db.session.add(autor)
        autor1 = Autor(nome='GeraldoJose',cpf=77777777,email='gg123@gmail.com',senha='Minhasenhafoda123',admin=False)
        db.session.add(autor1)
        autor2 = Autor(nome='JoaoGabriel',cpf=88888888,email='gokussj4@hotmail.com',senha='gokugokussjgogBlue2',admin=False)
        db.session.add(autor2)
        db.session.commit()

if __name__ == '__main__':
    inicializar_banco()

