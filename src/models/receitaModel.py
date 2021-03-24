
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="templates", static_folder="public")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receitas.sqlite3'

db = SQLAlchemy(app)


class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    ingredientes = db.Column(db.String(1000), nullable=False)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

if __name__ == "__main__":
    db.create_all()
    app.run()