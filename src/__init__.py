from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="templates", static_folder="public")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredientes.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///receitas.sqlite3'


db = SQLAlchemy(app)


class Ingrediente(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    qtd = db.Column(db.Integer)
    

    def __init__(self, nome, qtd):
        self.nome = nome
        self.qtd = qtd

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_receita = db.Column(db.String(50), unique=True, nullable=False)
    ingredientes = db.Column(db.String(1000), nullable=False)
    modo_preparo = db.column(db.String(5000))
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, nome_receita, ingrediente, modo_preparo):
        self.nome = nome
        self.ingrediente = ingrediente
        self.modo_preparo = modo_preparo

        

##### HOME #####
@app.route("/")
def home():
    return render_template("home.html")


##### PAGINA DO USUARIO #####
@app.route("/usuario")
def user():
    return render_template("Usuario.html")


##### ENVIAR RECEITA #####
@app.route("/enviar_receita")
def enviar_receita():
    return render_template("Enviar_receita.html")


##### INGREDIENTE #####
@app.route("/ingrediente")
def ingrediente():
    ingredientes = Ingrediente.query.all()
    return render_template("Ingredientes.html", ingredientes=ingredientes)


##### ADD INGREDIENTE ######
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        ingrediente = Ingrediente(request.form['nome'], request.form['qtd'])
        db.session.add(ingrediente)
        db.session.commit()
        return redirect(url_for("ingrediente"))
#    return render_template("add.html")


##### EDITAR INGREDIENTE #####
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    ingrediente = Ingrediente.query.get(id)
    if request.method == "POST":
        ingrediente.nome = request.form['nome']
        ingrediente.qtd = request.form["qtd"]
        db.session.commit()
        return redirect(url_for("ingrediente"))
    return render_template("edit.html", ingrediente=ingrediente)


##### DELETAR INGREDIENTE #####
@app.route("/delete/<int:id>")
def delete(id):
    ingrediente = Ingrediente.query.get(id)
    db.session.delete(ingrediente)
    db.session.commit()
    return redirect(url_for("ingrediente"))

######################### RECEITA ############################################
#@app.route("/receita")
#def receita():
#    ingredientes = Ingrediente.query.all()
#    return render_template("Receita.html", ingredientes=ingredientes)


######################### RECEITA ############################################
@app.route("/receita")
def receita():
    receita = pegar_receita()
    return render_template("Receita.html", receita=receita)



######################### RECEITA ############################################
@app.route("/add_receita", methods=["GET", "POST"] )
def pegar_receita():
    return [{
        'id':1,
        'name':'Bolo de chocolate',
        'ingrediente': {
            'ovo':'3',
            'oleo': '1 xicara',
            'chocolate':'1 barra'
            },'modo_preparo':'bata tudo no liquidicador, coloque em uma assadeira e leve ao forno por 30 minutos',
            'criado_em': '01/01/2021'
    }]


######################## RECEITA #######################################
#@app.route("/add", methods=["GET", "POST"])
#def add():
#    if request.method == "POST":
#        ingrediente = Ingrediente(request.form['nome'], request.form['qtd'])
#        db.session.add(ingrediente)
#        db.session.commit()
#        return redirect(url_for("receita"))
#    return render_template("add.html")


######################### RECEITA ######################################
#@app.route("/edit/<int:id>", methods=["GET", "POST"])
#def edit(id):
#    ingrediente = Ingrediente.query.get(id)
#    if request.method == "POST":
#        ingrediente.nome = request.form['nome']
#        ingrediente.qtd = request.form["qtd"]
#        db.session.commit()
#        return redirect(url_for("receita"))
#    return render_template("edit.html", ingrediente=ingrediente)


################# RECEITA ################################################
#@app.route("/delete/<int:id>")
#def delete(id):
#    ingrediente = Ingrediente.query.get(id)
#    db.session.delete(ingrediente)
#    db.session.commit()
#    return redirect(url_for("receita"))


if __name__ == "__main__":
    db.create_all()
    app.run()
