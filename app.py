from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# DB structure - table users, with user_id (serial, primary key), username (varchar(15)), email (varchar(255), unique), password (varchar(100))
def connect_to_db():
    connection = psycopg2.connect (
        host="localhost",
        database="project_crazy_accounts",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    return connection


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sign-up", methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        connection = connect_to_db()
        cursor = connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, password)'
                'VALUES (%s, %s, %s)',
                (username, email, password)
            )
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
        except psycopg2.IntegrityError:
            print("Email already exists!")
            cursor.close()
            connection.close()
            return render_template("signup.html", errors={"already_exists": True})

    return render_template("signup.html", errors={"already_exists": False})

@app.route("/log-in")
def login():
    return render_template("login.html")