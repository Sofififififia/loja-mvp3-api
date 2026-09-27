from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Pedido

app = Flask(__name__)
CORS(app)  # Libera requisições vindas de outras origens (ex: o front-end aberto como arquivo local)

# Configuração do banco SQLite: será criado um arquivo "loja.db" na pasta do projeto
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loja.db"
db.init_app(app)

# Cria as tabelas (se ainda não existirem) assim que a aplicação sobe
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return jsonify({"mensagem": "API de pedidos rodando!"})


# GET: listar todos os pedidos
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([pedido.to_dict() for pedido in pedidos])


# POST: criar um novo pedido
@app.route("/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json()

    novo_pedido = Pedido(
        titulo_produto=dados.get("titulo_produto"),
        preco_produto=dados.get("preco_produto"),
        imagem_produto=dados.get("imagem_produto"),
        quantidade=dados.get("quantidade", 1),
    )

    db.session.add(novo_pedido)
    db.session.commit()

    return jsonify(novo_pedido.to_dict()), 201


# PUT: atualizar um pedido existente (ex: mudar status)
@app.route("/pedidos/<int:pedido_id>", methods=["PUT"])
def atualizar_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)

    if pedido is None:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    dados = request.get_json()
    pedido.status = dados.get("status", pedido.status)
    pedido.quantidade = dados.get("quantidade", pedido.quantidade)

    db.session.commit()

    return jsonify(pedido.to_dict())


# DELETE: remover um pedido
@app.route("/pedidos/<int:pedido_id>", methods=["DELETE"])
def deletar_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)

    if pedido is None:
        return jsonify({"erro": "Pedido não encontrado"}), 404

    db.session.delete(pedido)
    db.session.commit()

    return jsonify({"mensagem": f"Pedido {pedido_id} removido com sucesso"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)