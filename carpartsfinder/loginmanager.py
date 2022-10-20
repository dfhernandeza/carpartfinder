from pickle import TRUE
from carpartsfinder import app
from carpartsfinder.helpers import apology, login_master_required, login_required, SQL
import json
from msilib.schema import Error
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize sql class
db = SQL("database.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":        
        # store request parameters into variables
        firstName = request.form.get("first_name").upper()
        lastName = request.form.get("last_name").upper()
        phoneNumber = request.form.get("phone_number").upper()
        address = request.form.get("address").upper()
        email = request.form.get("email").lower()       
        password = request.form.get("password")
                   
                  
        db.execute("INSERT INTO users (hash, email, first_name, last_name, phone_number, address, rol) VALUES (?, ?, ?, ?, ?, ?, 'user')",
         (generate_password_hash(password), email, firstName, lastName, phoneNumber, address))
    
        return redirect("/login")
    else:
        return render_template("register.html")   

@app.route("/emailvalidation")
def emailValidation():
    email = request.args.get("email")
    result = db.execute("SELECT COUNT(email) count FROM users WHERE email = ?",[email])[0]["count"]
    if result == 0:
        return jsonify(True)
    else:
        return jsonify(False)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", [request.form.get("email")])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_rol"] = rows[0]["rol"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/changepassword", methods=["GET","POST"])
@login_required
def changepassword():
    iduser = session["user_id"]
    if request.method == "GET":        
        return render_template("changepassword.html")
    else:
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        dbpassword = db.execute("SELECT hash FROM users WHERE id = ?", (iduser,))
        if check_password_hash(dbpassword[0]["hash"], oldpassword):
            db.execute("UPDATE users SET hash = ? WHERE id = ?",(generate_password_hash(newpassword), iduser))
            return jsonify(True)
        else:
            return jsonify(False)

