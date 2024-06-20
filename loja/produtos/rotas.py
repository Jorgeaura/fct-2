# loja/produtos/rotas.py
from flask import render_template, redirect, url_for, flash, request
from loja import app, db
from loja.produtos.models import Produto


@app.route('/produto', methods=['GET', 'POST'])
def produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        preco = request.form.get('preco', type=float)
        image_url = request.form.get('image_url')
        categoriaId = request.form.get('categoriaId', type=int)

        novo_produto = Produto(
            descricao=descricao,
            preco=preco,
            image_url=image_url,
            categoriaId=categoriaId
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('index'))
    return render_template('produto.html')
