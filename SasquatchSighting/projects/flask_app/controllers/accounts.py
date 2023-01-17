from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.account import Account
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not Account.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Account.save(data)
    session['account_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    account = Account.get_by_email(request.form)

    if not account:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(account.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['account_id'] = account.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    if 'account_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['account_id']
    }
    return render_template("dashboard.html", account = Account.get_by_id(data), bands = Sighting.get_all(), check = Account.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')