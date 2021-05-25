from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import select

app = Flask(__name__, template_folder="templates", static_folder="public")
app.config.from_object('config')

db = SQLAlchemy(app)

##### CRIANDO A TABLE RECEITA_INGREDIENTE #####
receita_ingrediente = db.Table('receita_ingrediente',
   db.Column('receita_id', db.Integer, db.ForeignKey('receita.receita_id')),
   db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.ingrediente_id')),
   db.Column('qtd', db.String())
)


##### CRIANDO A TABLE RECEITA #####
class Receita(db.Model):
   __tablename__ = 'receita'

   receita_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(), nullable=False)
   modo_preparo = db.Column(db.String(), nullable=False)
   ingredientes = db.relationship('Ingrediente', secondary=receita_ingrediente, lazy='subquery',
    backref=db.backref('receita', lazy=True))    

   def __init__(self, nome, modo_preparo):
       self.nome = nome
       self.modo_preparo = modo_preparo
            

   def __repr__(self):
       return '{}'.format(self.nome)
       

   def serialize(self):
       return {
           'id': self.receita_id, 
           'nome': self.nome,
           'modo_preparo':self.modo_preparo
            }


##### CRIANDO A TABLE INGREDIENTE #####
class Ingrediente(db.Model):
   __tablename__ = 'ingrediente'

   ingrediente_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   nome = db.Column(db.String(), unique=True, nullable=False )

   def __init__(self, nome):
       self.nome = nome

   def __repr__(self):
       return '{}'.format(self.nome)

   def serialize(self):
       return {
           'id': self.id, 
           'nome': self.nome,
       }

 
##### HOME #####
@app.route("/")
def home():
    return render_template("home.html")

##### PAGINA DO USUARIO #####
@app.route("/usuario")
def user():
    return render_template("Usuario.html")

##### MINHAS RECEITAS RECEITA #####
@app.route("/minhas_receitas")
def minhas_receitas():
    return render_template("Minhas Receitas.html")

##### INGREDIENTE #####
@app.route("/ingrediente")
def ingrediente():
    ingredientes = Ingrediente.query.all()
    return render_template("Ingredientes.html", ingredientes=ingredientes)

##### ADD INGREDIENTE ######
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        ingrediente = Ingrediente(request.form['nome'])
        db.session.add(ingrediente)
        db.session.commit()
        return redirect(url_for("ingrediente"))

##### EDITAR INGREDIENTE #####
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    ingrediente = Ingrediente.query.get(id)
    if request.method == "POST":
        ingrediente.nome = request.form['nome']
        db.session.commit()
        return redirect(url_for("ingrediente"))
    return render_template("edit_ingrediente.html", ingrediente=ingrediente)

##### DELETAR INGREDIENTE #####
@app.route("/delete/<int:id>")
def delete(id):
    ingrediente = Ingrediente.query.get(id)
    db.session.delete(ingrediente)
    db.session.commit()
    return redirect(url_for("ingrediente"))

##### RECEITA #####
@app.route("/receita")
def receita():
    receitas = Receita.query.all()
    return render_template("receitas.html", receitas=receitas)

##### ADD RECEITA ######
@app.route("/add_receita", methods=["GET", "POST"])
def add_receita():
    if request.method == "POST":
        receita = Receita(request.form['nome'], request.form['modo_preparo'])
        db.session.add(receita)
        db.session.commit()
        return redirect(url_for("receita"))

##### EDITAR RECEITA #####
@app.route("/edit_receita/<int:id>", methods=["GET", "POST"])
def edit_receita(id):
    receita = Receita.query.get(id)
    if request.method == "POST":
        receita.nome = request.form['nome']
        receita.modo_preparo = request.form['modo_preparo']
        db.session.commit()
        return redirect(url_for("receita"))
    return render_template("edit_receita.html", receita=receita)

##### DELETAR INGREDIENTE #####
@app.route("/delete_receita/<int:id>")
def delete_receita(id):
    receita = Receita.query.get(id)
    db.session.delete(receita)
    db.session.commit()
    return redirect(url_for("receita"))

##### ADICIONAR ITENS RECEITA #####
@app.route("/itens_receita/<int:id>", methods=["GET", "POST"])
def itens_receita(id):
    receita = Receita.query.get(id)
    if request.method == "POST":
        i=Ingrediente.query.filter_by(nome=(request.form['ingrediente_id'])).first()
        receita.ingredientes.append(i)
        db.session.commit()
        return redirect(url_for("itens_receita", id = id))
    return render_template("itens_receita.html", receita=receita)


if __name__ == "__main__":
    db.create_all()
    app.run()
