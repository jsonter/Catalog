from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random, string, requests, json, httplib2
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from database_setup import Base, User, Category, Item

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in login_session:
            return f(*args, **kwargs)
        else:
            flash('You are not logged in!')
            return redirect(url_for('catalog'))
    return decorated_function

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't; make a new one.
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    # If user found, add the user id to the session. If new user cannot be added, disconnect the google account.
    if user_id:
        login_session['user_id'] = user_id
    else:
        return redirect(url_for('gdisconnect'))

    flash("Successfully connected")
    return redirect(url_for('catalog'))


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['credentials']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('catalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('catalog'))

@app.route('/')
@app.route('/catalog')
@app.route('/category/<int:category_id>')
def catalog(category_id = 0):
    login_session['state'] = state
    categories = session.query(Category).all()
    if category_id:
        category = session.query(Category).filter_by(id = category_id).one()
        items = session.query(Item).filter_by(category_id = category_id)
    else:
        category = ''
        items = session.query(Item).order_by(Item.id.desc()).limit(5)

    #userId = ''
    #userName = ''
    #login_picture = ''
    #if 'user_id' in login_session:
#        userId = login_session['user_id']
#        userName = login_session["username"]
#        login_picture = login_session["picture"]
    if 'user_id' in login_session:
        user = getUserInfo(login_session['user_id'])
        return render_template('catalog.html', user = user, categories = categories, category = category, items = items, STATE = login_session["state"])
    else:
        return render_template('catalog.html', user = '', categories = categories, category = category, items = items, STATE = login_session["state"])

#    return render_template('catalog.html', user_id = userId, user_name = userName, picture = login_picture, categories = categories, category = category, items = items, STATE = login_session["state"])

@app.route('/catalog.json')
def catalogJSON(category_id = False):
    categories = session.query(Category).all()
    serializedCategories = []
    for i in categories:
        newCategory = i.serialize
        items = session.query(Item).filter_by(category_id = i.id).all()
        serializedItems = []
        for j in items:
            serializedItems.append(j.serialize)
        newCategory['items'] = serializedItems
        serializedCategories.append(newCategory)
    return jsonify(categories=[serializedCategories])

#@app.route('/category/<int:category_id>')
#def category(category_id):
#    categories = session.query(Category).all()
#    category = session.query(Category).filter_by(id = category_id).one()
#    items = session.query(Item).filter_by(category_id=category_id)
#    user = getUserInfo(login_session["user_id"])
#    return render_template('catalog.html', user = user, categories = categories, category = category, items = items, STATE = state)

@app.route('/category/new', methods=['GET','POST'])
@login_required
def newCategory():
    if request.method == 'POST':
        newCategory = Category(
            name = request.form['category'],
            user_id = login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("New category created!")
        return redirect(url_for('catalog'))
    else:
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('newCategory.html', user = user)
        else:
            return render_template('newCategory.html', user = '')

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
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('editCategory.html', user = user, category = category)
        else:
            return render_template('editCategory.html', user = '', category = category)

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
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('deleteCategory.html', user = user, category = category)
        else:
            return render_template('deleteCategory.html', user = '', category = category)

@app.route('/category/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(id = item_id).one()
    if 'user_id' in login_session:
        user = getUserInfo(login_session['user_id'])
        return render_template('showItem.html', user = user, item = item)
    else:
        return render_template('showItem.html', user = '', item = item)

@app.route('/item/new', methods=['GET','POST'])
@login_required
def newItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Item(
            name = request.form['name'],
            description = request.form['description'],
            category_id = request.form['category_id'],
            user_id = login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New item created!")
        return redirect(url_for('catalog'))
    else:
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('newItem.html', user = user, categories = categories)
        else:
            return render_template('newItem.html', user = '', categories = categories)

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
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('editItem.html', user = user, item = item, categories = categories)
        else:
            return render_template('editItem.html', user = '', item = item, categories = categories)

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
        if 'user_id' in login_session:
            user = getUserInfo(login_session['user_id'])
            return render_template('deleteItem.html', user = user, item = item)
        else:
            return render_template('deleteItem.html', user = '', item = item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return "The current session state is %s" %login_session['state']


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del login_session['credentials']
    del login_session['gplus_id']
    del login_session['user_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    return "Logged out"

# Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# User Info
def getUserId(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUser(login_session):
    try:
        newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
        session.add(newUser)
        session.commit()
        user = session.query(User).filter_by(email = login_session['email']).one()
        flash("Welcome %s, you have been added as a new user." %user.name)
        return user.id
    except:
        session.rollback()
        flash("Could not store new user!")
        return None

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.username = 'admin'
    app.password = 'a'
    app.loggedIn = False
    app.run(host = '0.0.0.0', port = 5000)
