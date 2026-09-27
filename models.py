from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo_produto = db.Column(db.String(200), nullable=False)
    preco_produto = db.Column(db.Float, nullable=False)
    imagem_produto = db.Column(db.String(500), nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), nullable=False, default="pendente")
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo_produto": self.titulo_produto,
            "preco_produto": self.preco_produto,
            "imagem_produto": self.imagem_produto,
            "quantidade": self.quantidade,
            "status": self.status,
            "data_criacao": self.data_criacao.isoformat(),
        }