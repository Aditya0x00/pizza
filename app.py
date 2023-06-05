from flask import Flask, render_template, session, request, redirect
import sqlite3 as sql

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'poornima123456789'

con = sql.connect('pizzas.db')
cursor = con.cursor()
con.execute('CREATE TABLE IF NOT EXISTS users (username varchar unique, password varchar);')
con.execute('CREATE TABLE IF NOT EXISTS pizzas (pizza_id integer primary key, );')
con.execute('CREATE TABLE IF NOT EXISTS orders ();')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = con.execute("SELECT * FROM users WHERE username=? AND password=?;", (username, password)).fetchone()
        if user is not None:
            session['username'] = username
            return redirect('/')
        else:
            return render_template("login.html", error="Invalid Username or Password")
    return render_template("login.html")

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']
        if password==cpassword:
            con.execute("INSERT INTO users VALUES (?,?);", (username, password))
            session['username'] = username
            return redirect('/')
        else:
            return render_template("register.html", error="Password and Confirm Password don't match")
    return render_template("register.html")

@app.route('/pizzas')
def pizzas():
    return render_template("pizzas.html")

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
