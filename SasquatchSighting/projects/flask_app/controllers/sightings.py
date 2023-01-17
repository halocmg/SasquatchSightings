import re
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.account import Account

@app.route('/new/sighting')
def newsighting():

    return render_template("newsighting.html")


@app.route('/sightinglog',methods=['POST'])
def report():
    if not Sighting.validate_register(request.form):
        return redirect('/new/sighting')
    data ={ 
        "location": request.form['location'],
        "time": request.form['time'],
        "description": request.form['description'],
        "amount": request.form['amount'],
        "account_id": session['account_id']
        }
    
    Sighting.save(data)
    
    return redirect('/dashboard')

@app.route('/sightingedit',methods=['POST'])
def replace():
    if not Sighting.validate_register(request.form):
        return redirect(f"/edit/{request.form['id']}")
    data ={
        "id":request.form['id'],
        "location": request.form['location'],
        "time": request.form['time'],
        "description": request.form['description'],
        "amount": request.form['amount'],
        }
    Sighting.replace(data)
    
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def showsightings(id):
    data ={ 
        "id":id,
    }
    return render_template("showsighting.html", user= Sighting.get_by_id(data), check = Account.get_all())

@app.route('/edit/<int:id>')
def editsightings(id):
    data ={ 
        "id":id,
    }
    return render_template("editsighting.html", user= Sighting.get_by_id(data))

@app.route('/destroy/<int:id>')
def removal(id):
    data ={
        "id":id
    }
    Sighting.delete(data)
    return redirect('/dashboard')



