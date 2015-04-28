from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if app.loggedIn == True:
            return f(*args, **kwargs)
        else:
            flash('You are not logged in!')
            return redirect(url_for('catalog'))
    return decorated_function

@app.route('/')
@app.route('/categories')
@app.route('/category/<int:category_id>')
def catalog(category_id = False):
    if category_id == False:
        categories = session.query(Category).all()
        category = False
        items = session.query(Item).order_by(Item.id.desc()).limit(7)
        return render_template('catalog.html', loggedIn = app.loggedIn, categories = categories, category = category, items = items)
    else:
        categories = session.query(Category).all()
        category = session.query(Category).filter_by(id = category_id).one()
        items = session.query(Item).filter_by(category_id=category_id)
        return render_template('catalog.html', loggedIn = app.loggedIn, categories = categories, category = category, items = items)

@app.route('/category/new', methods=['GET','POST'])
@login_required
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
@login_required
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
@login_required
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash("Category deleted!")
        return redirect(url_for('catalog'))
    else:
        return render_template('deleteCategory.html', category = category)

@app.route('/category/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    return render_template('showItem.html', item = item)

@app.route('/item/new', methods=['GET','POST'])
@login_required
def newItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name = request.form['name'],
            description = request.form['description'],
            category_id = request.form['category_id'])
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('catalog'))
    else:
        return render_template('newItem.html', categories = categories)

@app.route('/item/<int:item_id>/edit', methods=['GET','POST'])
@login_required
def editItem(item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        item.name =request.form['name']
        item.description = request.form['description']
        item.category_id = request.form['category_id']
        session.commit()
        flash("Item modified!")
        return redirect(url_for('catalog'))
    else:
        return render_template('editItem.html', item = item, categories = categories)

@app.route('/item/<int:item_id>/delete', methods=['GET','POST'])
@login_required
def deleteItem(item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item deleted!")
        return redirect(url_for('catalog'))
    else:
        return render_template('deleteItem.html', item = item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.username:
            error = 'Invalid username'
        elif request.form['password'] != app.password:
            error = 'Invalid password'
        else:
            app.loggedIn = True
            flash('You were logged in')
            return redirect(url_for('catalog'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    app.loggedIn = False
    flash('You were logged out')
    return redirect(url_for('catalog'))


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
    app.username = 'admin'
    app.password = 'a'
    app.loggedIn = False
    app.run(host = '0.0.0.0', port = 5000)
