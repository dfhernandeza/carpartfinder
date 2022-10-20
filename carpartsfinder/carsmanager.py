from carpartsfinder import app
from carpartsfinder.helpers import apology, login_master_required, login_required, SQL, is_master
import json
from msilib.schema import Error
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize sql class
db = SQL("database.db")

# renders page for the management of car makes, models and years available
@app.route("/managecars")
@login_master_required
def carsmanager():
    years = db.execute("SELECT id, year text FROM years")
    return render_template("managecars.html", years = years)
# validates car make availability (avoid repetition)
@app.route("/carmakevalidation")
@login_master_required
def carmakevalidation():
    make = request.args.get("make")
    make = '%' + make + '%'
    result = db.execute("SELECT COUNT(id) count FROM car_makes WHERE make = ?",[make])[0]["count"]
    if result == 0:
        return jsonify(True)
    else:
        return jsonify(False)
# inserts a new car make in the database
@app.route("/newcarmake", methods=["POST"])
@login_master_required
def newcarmake():
    make = request.form.get("make").upper()     
    try:
        db.execute("INSERT INTO car_makes (make) VALUES (?)",[make])
    except Error as err:
        return jsonify(err)
    return jsonify(True)              
# updates a car make in the database
@app.route("/editcarmake", methods=["POST"])
@login_master_required
def editcarmake():
    make = request.form.get("make").upper()
    id = request.form.get("id").upper()
    try:
        db.execute("UPDATE car_makes SET make = ? WHERE id = ?", (make, id))
    except:
        return jsonify(False)
    return jsonify(True)
# deletes a car make from the database
@login_master_required
@app.route("/deletecarmake", methods=["POST"])
def deletecarmake():    
    id = request.form.get("id")
    try:
        db.execute("DELETE FROM car_makes WHERE id = ?", (id,))
        return jsonify(True)
    except:
        return jsonify(False)
# returns all car makes in the database (json)  
@app.route("/getcarmakes", methods=["GET","POST"])
@login_master_required
def getcarmakes():
    try:
        data = db.execute("SELECT * FROM car_makes ORDER BY make")
        return jsonify(data)   
    except:
        return jsonify("Error")
# returns all car models for the provided make         
@app.route("/getcarmodels", methods=["GET","POST"])
@login_master_required
def getcarmodels():
    carmakeid = request.form.get("carmakeid")  
    data = db.execute("SELECT * FROM car_models WHERE car_make_id = ? ORDER BY car_model",[carmakeid])    
    return jsonify(data)  
# inserts new model for the provided make
@app.route("/newcarmodel", methods=["POST"])
@login_master_required
def newcarmodel():
    carmodel = request.form.get("carmodel").upper()
    car_make_id = request.form.get("carmakeid")     
    try:
        db.execute("INSERT INTO car_models (car_model, car_make_id) VALUES (?, ?)",(carmodel, car_make_id))
    except Error as err:
        return jsonify(err)
    return jsonify(True)  
# updates car model
@app.route("/editcarmodel", methods=["POST"])
@login_master_required
def editcarmodel():
    carmodel = request.form.get("carmodel")
    id = request.form.get("idmodel")     
    try:
        db.execute("UPDATE car_models SET car_model = ? WHERE id = ?",(carmodel.upper(), id))
        return jsonify(True)
    except:
        return jsonify(False)
# deletes car model     
@app.route("/deletecarmodel", methods=["POST"])
@login_master_required
def deletecarmodel():
    id = request.form.get("id")
    try: 
        db.execute("DELETE FROM car_models WHERE id = ?",(id,))
        return jsonify(True)
    except:
        return jsonify(False)
# validates car model availability (avoid repetition)
@app.route("/carmodelvalidation", methods=["POST"])
@login_master_required
def carmodelvalidation():
    model = request.form.get("carmodel")
    model = '%' + model + '%'
    carmakeid = request.form.get("carmakeid")
    result = db.execute("SELECT COUNT(id) count FROM car_models WHERE car_model = ? and car_make_id = ?",(model , carmakeid))[0]["count"]
    if result == 0:
        return jsonify(True)
    else:
        return jsonify(False)
# validates year availability (avoid repetition)
@app.route("/modelyearvalidation", methods=["POST"])
@login_master_required
def modelyearvalidation():
    idyear = request.form.get("idyear")
    idmodel = request.form.get("idmodel")
    result = db.execute("SELECT COUNT(id) count FROM model_year WHERE id_year = ? and id_model = ?",(idyear , idmodel))[0]["count"]
    if result == 0:
        return jsonify(True)
    else:
        return jsonify(False)
# returns years for a given model (json)
@app.route("/getyearsmodel", methods=["POST"])
@login_master_required
def getyears():
    idmodel = request.form.get("idmodel")
    data = db.execute("SELECT model_year.id, years.year FROM years INNER JOIN model_year ON years.id = model_year.id_year WHERE model_year.id_model = ? order by years.year asc", [idmodel])
    return jsonify(data)
# inserts a new year for a given model
@app.route("/newyearmodel", methods=["POST"])
@login_master_required
def newyearmodel():
    idyear = request.form.get("id_year")
    idmodel = request.form.get("id_model")
    result = db.execute("SELECT COUNT(id) count FROM model_year WHERE id_year = ? and id_model = ?",(idyear , idmodel))[0]["count"]
    if result == 0:
        db.execute("INSERT INTO model_year (id_year, id_model) VALUES (?, ?)", (idyear, idmodel))
        return jsonify(True)
    else:
        return jsonify(False)
# deletes a year for a given model
@app.route("/deletemodelyear", methods=["POST"])
@login_master_required
def deletemodelyear():
    id = request.form.get("id")
    try:
        db.execute("DELETE FROM model_year WHERE id = ?",(id,))
        return jsonify(True)
    except:
        return jsonify(False)