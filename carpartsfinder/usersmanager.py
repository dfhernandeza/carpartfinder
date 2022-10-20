from carpartsfinder import app
from carpartsfinder.helpers import apology, login_master_required, SQL, login_required
import json
from msilib.schema import Error
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize sql class
db = SQL("database.db")


@app.route("/manageusers")
@login_master_required
def usersmanager():
    return render_template("manageusers.html")


@app.route("/getUser")
@login_master_required
def get_users():
    email = request.args.get("email")
    iduser = request.args.get("iduser")
    data = []
    if not iduser:
        data = db.execute("SELECT first_name || ' ' || last_name name, first_name, last_name, email, rol, phone_number, address, id FROM users WHERE email = ?", [email])
        if len(data) == 0:
            return jsonify(False)
        else:
            return jsonify(data[0])
    else:
        data = db.execute("SELECT first_name || ' ' || last_name name, first_name, last_name, email, rol, phone_number, address, id FROM users WHERE id = ?", [iduser])
        return jsonify(data[0])


@app.route("/updatename", methods = ["POST"])
@login_master_required
def updateName():
    firstName = request.form.get("first_name")
    lastName = request.form.get("last_name")
    id = request.form.get("id")
    try:
        db.execute("UPDATE users SET first_name = ?, last_name = ? WHERE id = ?",(firstName.upper(), lastName.upper(), id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)
    

@app.route("/updateemail", methods = ["POST"])
@login_master_required
def updateMail():
    email = request.form.get("email")
    id = request.form.get("id")
    try:
        db.execute("UPDATE users SET email = ? WHERE id = ?",(email.lower(), id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)


@app.route("/updatephonenumber", methods = ["POST"])
@login_master_required
def updatePhoneNumber():
    phoneNumber = request.form.get("phone_number")
    id = request.form.get("id")
    try:
        db.execute("UPDATE users SET phone_number = ? WHERE id = ?",(phoneNumber, id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)


@app.route("/updaterol", methods = ["POST"])
@login_master_required
def updateRol():
    rol = request.form.get("rol")
    id = request.form.get("id")
    try:
        db.execute("UPDATE users SET rol = ? WHERE id = ?",(rol, id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)


@app.route("/updateaddress", methods = ["POST"])
@login_master_required
def updateAddress():
    address = request.form.get("address")
    id = request.form.get("id")
    try:
        db.execute("UPDATE users SET address = ? WHERE id = ?",(address.upper(), id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)


@app.route("/accountmanager")
@login_required
def accountmanager():
    iduser = session["user_id"]
    userinfo = db.execute("SELECT first_name || ' ' || last_name name, first_name, last_name, email, rol, phone_number, address, id FROM users WHERE id = ?", [iduser])[0]
    return render_template("accountmanager.html", userinfo = userinfo)