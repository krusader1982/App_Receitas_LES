from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="templates", static_folder="public")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredientes.sqlite3'

db = SQLAlchemy(app)

class Ingrediente(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    qtd = db.Column(db.Integer)
    passos = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


if __name__ == "__main__":
    db.create_all()
    app.run()