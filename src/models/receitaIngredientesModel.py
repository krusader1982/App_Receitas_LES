from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReceitaIngredientes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ingrediente = db.Column(db.Integer, nullable=False)
    id_receita = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
