import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__, template_folder="./static")

Myclient = MongoClient(
	os.environ['DB_PORT_27017_TCP_ADDR'],
	27017)
Database = Myclient["mydatabase"]
Collection = Database["account"]

token = {"name":"","email":"","password":""}

@app.route('/')
def root():
	return render_template('register.html')

@app.route('/register',methods = ['POST'])
def register():
	item_doc = {
		'name': request.form['name'],
		'email': request.form['email'],
		'password': request.form['password']
	}

	Collection.insert_one(item_doc)

	return render_template("register.html", items="Successful")

@app.route('/signinScreen',methods = ['POST'])
def loginScreen():
	return render_template("signin.html")

@app.route('/signin',methods = ['POST'])
def login():
	global token
	item_doc = {
		'name': request.form['name'],
		'password': request.form['password']
	}

	retval = Collection.find_one(item_doc ,{"_id":0})

	if retval == None:
		items = "Error"
		return render_template("signin.html",items = items)


	token["name"] = retval["name"]
	token["email"] = retval["email"]
	token["password"] = retval["password"]
	
	return render_template("main.html",name = token["name"])

	

@app.route('/registerScreen',methods = ['POST'])
def signupScreen():
	return render_template("register.html")


@app.route('/changePassword',methods = ['POST'])
def changePassword():
	global token

	newPassword = {
		'password': request.form['password']
	}

	newValues = { "$set":newPassword}
	Collection.update_one(token, newValues)

	token["password"] = newPassword["password"]

	return render_template("main.html",info = token["password"], name = token["name"])

@app.route('/changeEmail',methods = ['POST'])
def changeEmail():
	global token

	newEmail = {
		'email': request.form['email']
	}

	newValues = { "$set":newEmail}
	Collection.update_one(token, newValues)

	token["email"] = newEmail["email"]

	return render_template("main.html",info = token["email"] , name= token["name"] )

@app.route('/getInfo',methods = ['POST'])
def getInfo():
	global token
	return render_template("main.html",info = token, name = token["name"])

@app.route('/out',methods = ['POST'])
def out():
	global token
	token["name"] = ""
	token["email"] = ""
	token["password"] =""

	return render_template("register.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)