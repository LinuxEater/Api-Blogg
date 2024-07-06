from flask import Flask,jsonify,request,make_response
from meuprimeiro_DataBase import Autor,application,Postagem,db
import jwt
from datetime import datetime,timedelta
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem':'token não foi encontrado'},401)
        try:
            resultado = jwt.decode(token,application.config['SECRET_KEY'],algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()        
        except:
            return jsonify({'mensagem':'Token é invalido'},401)
        return f(autor,*args,**kwargs)
    return decorated


@application.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login Invalido',401,{'WWW-Authenticate':'Basic realm="Login Obrigatorio"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login Invalido',401,{'WWW-Authenticate':'Basic realm="Login Obrigatorio"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor':usuario.id_autor,'exp':datetime.utcnow() + timedelta(minutes=30)},application.config['SECRET_KEY'])
        return jsonify({'token':token})
    return make_response('Login Invalido',401,{'WWW-Authenticate':'Basic realm="Login Obrigatorio"'})


@application.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome'] = autor.nome
        autor_atual['cpf'] = autor.cpf
        autor_atual['email'] = autor.email
        autor_atual['senha'] = autor.senha
        lista_de_autores.append(autor_atual)
    return jsonify({'autores':lista_de_autores})    


#obter autores por id
@application.route('/autores/<int:id_autor>',methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f"Autor inexistente!")
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome'] = autor.nome
    autor_atual['cpf'] = autor.cpf
    autor_atual['email'] = autor.email
    autor_atual['senha'] = autor.senha

    return jsonify({'autor':autor_atual})
    

#criar autores com id com POST
@application.route('/autores',methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()

    autor = Autor(nome=novo_autor['nome'],senha=novo_autor['senha'],email=novo_autor['email'],cpf=novo_autor['cpf'])

    db.session.add(autor)
    db.session.commit()
    return({'Mensagem':'Usuario criado com sucesso!'},200)


#modificar um autor com PUT
@application.route('/autores/<int:id_autor>',methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor,id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({'Mensagem':'Usuario não encontrado!'})
    try:
        if usuario_a_alterar['nome']:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass        
    try:
        if usuario_a_alterar['email']:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:        
        if usuario_a_alterar['cpf']:
            autor.cpf = usuario_a_alterar['cpf']
    except:
        pass
    try:        
        if usuario_a_alterar['senha']:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass        
    db.session.commit()
    return jsonify({'Mensagem':'Usuario alterado com sucesso!'})            


#excluir um autor com DELETE
@application.route('/autores/<int:id_autor>',methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor,id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'Mensagem':'Este autor não existe!'})
    db.session.commit()
    return jsonify({'Mensagem':'Autor Excluido com sucesso.'})
    

#rodando o aplicativo em uma porta,em um host especificados e com o modo debugging ativado
application.run(port=5000,host='localhost',debug=True)