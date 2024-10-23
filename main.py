import json
from flask import Flask, Response, request
# Conexão com o banco de dados
from flask_sqlalchemy import SQLAlchemy
 

# Aplicação do tipo Flask
app = Flask('carros')

# Haverá MODIFICAÇÕES no nosso banco de dados, por padrão fica em FALSE 
app.config['SQLALCHEMY_TRACK_MODICATIONS'] = True

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_carro'

#  Configuramos a variavel que representará o banco
mybd = SQLAlchemy(app)

# Definimos a estrutura da tabela tb_carros
class Carros(mybd.Model):
    __tablename__ = 'tb_carros'
    id = mybd.Column(mybd.Integer, primary_key = True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float) 
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(10))


    def to_json(self): # Convertemos a tabela em JSON
        return{ 
        "id":self.id,
        "marca":self.marca,
        "modelo":self.modelo,
        "valor":self.valor,
        "cor":self.cor,
        "numero_vendas":self.numero_vendas,
        "ano":self.ano
        } 


# API
# Selecionar tudo (GET)
@app.route("/carros",methods=["GET"])
def selecionar_carros():
    # Executa uma consulta no banco de dados para obter todos os registros 
    # o método query.all retorna uma lista de objetos "carros"
    carro_objetos = Carros.query.all()
    
    carro_json = [carro.to_json() for carro in carro_objetos]

    return gera_response(200, "carros", carro_json)


#Selecionar individual por ID
@app.route("/carros/<id>", methods=["GET"])
def seleciona_carro_id(id):
    carro_objetos = Carros.query.filter_by(id=id).first()
    carro_json = carro_objetos.to_json()

    return gera_response(200, "carros", carro_json)


# Cadastrar
@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()

    try:
        carro = Carros(id=body["id"], 
                       marca=body["marca"],
                       modelo=body["modelo"],
                       valor=body["valor"], 
                       cor=body["cor"],
                       numero_vendas=body["numero_vendas"], 
                       ano=body["ano"])
        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com Sucesso!!!")
    
    except Exception as e:
        print("Erro", e)

        return gera_response(400, "carros", {}, "Erro ao cadastrar !")
    

#Atualizar
@app.route("/carros/<id>", methods=["PUT"])
def atualizar_carro(id):
    # Consulta por ID
    carro_objetos = Carros.query.filter_by(id=id).first()

    # Corpo da requisição
    body = request.get_json()

    try:
        if('marca' in body):
            carro_objetos.marca = body['marca']
        if('modelo' in body):
            carro_objetos.modelo = body['modelo']
        if('valor' in body):
            carro_objetos.valor = body['valor']
        if('cor' in body):
            carro_objetos.cor = body['cor']
        if('numero_vendas' in body):
            carro_objetos.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objetos.ano = body['ano']

        mybd.session.add(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Atualizado com Sucesso !!!")
    
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, "Erro ao Atualizar")

# Deletar
@app.route("/carros/<id>", methods=["DELETE"])
def deletar_carro(id):
    carro_objetos = Carros.query.filter_by(id=id).first()

    try:
        mybd.session.delete(carro_objetos)
        mybd.session.commit()

        return gera_response(200, "carros", carro_objetos.to_json(), "Deletado com Sucesso !!!")
    
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carro", {}, "Erro ao Deletar")
    


def gera_response(status, nome_conteudo, conteudo, mensagem= False):
    body = {}
    body[nome_conteudo] = conteudo
    
    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json") 


app.run(port=5000,host='localhost',debug=True)


