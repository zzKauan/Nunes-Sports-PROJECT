from flask import Flask, render_template, request, redirect, url_for
from models import db, Produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/add', methods=['POST'])
def add_produto():
    nome = request.form.get('nome')
    codigo = request.form.get('codigo')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')
    novo_produto = Produto(nome=nome, codigo=codigo, descricao=descricao, preco=preco)
    db.session.add(novo_produto)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_produto(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
