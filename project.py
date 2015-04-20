from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/categories')
@app.route('/category/<int:category_id>')
def catalog(category_id = False):
    if category_id == False:
        categories = session.query(Category).all()
        category = False
        items = session.query(Item).order_by(Item.id.desc()).limit(7)
        return render_template('catalog.html', categories = categories, category = category, items = items)
    else:
        categories = session.query(Category).all()
        category = session.query(Category).filter_by(id = category_id).one()
        items = session.query(Item).filter_by(category_id=category_id)
        return render_template('catalog.html', categories = categories, category = category, items = items)

@app.route('/category/new', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name = request.form['category'])
        session.add(newCategory)
        session.commit()
        flash("New category created!")
        return redirect(url_for('catalog'))
    else:
        return render_template('newCategory.html')

@app.route('/category/<int:category_id>/edit', methods=['GET','POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        category.name = request.form['category']
        session.commit()
        flash("Category name changed!")
        return redirect(url_for('catalog'))
    else:
        return render_template('editCategory.html', category = category)

@app.route('/category/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash("Category deleted!")
        return redirect(url_for('catalog'))
    else:
        return render_template('deleteCategory.html', category = category)


@app.route('/category/<int:category_id>/items')
def showItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    return render_template('showItems.html', category = category)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
