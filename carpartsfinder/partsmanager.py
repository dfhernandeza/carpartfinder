from operator import methodcaller
from carpartsfinder import app
from carpartsfinder.helpers import apology, login_master_required, login_required, SQL
import json
from msilib.schema import Error
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests
from flask_session import Session
from carpartsfinder.blobsaccess import upload, delete
# Initialize sql class
db = SQL("database.db")

@app.route("/sell", methods=["GET"])    
@login_required
def sell():
    cars = db.execute("SELECT * FROM car_makes")
    return render_template("sell.html", cars = cars)

@app.route("/getModels", methods=["POST"])    
@login_required
def getModels():
    idmake = request.form.get("idmake")
    models = db.execute("SELECT car_model text, id FROM car_models WHERE car_make_id = ?",[idmake])
    return jsonify(models)

@app.route("/getYears", methods=["POST"])    
@login_required
def getYears():
    idmodel = request.form.get("idmodel")
    years = db.execute("SELECT model_year.id_year id, years.year text FROM model_year INNER JOIN years on model_year.id_year = years.id WHERE model_year.id_model = ?",[idmodel])
    return jsonify(years)

@app.route("/upload", methods=["POST"])    
@login_required
def uploadfile():
    part = json.loads(request.form.get('object'))

    # New part for sale
    part_name = part["part_name"].upper()
    price = part["price"]
    description = part["description"].upper()
    idpart = db.execute_returnid("INSERT INTO parts (part_name, id_user, price, description, date, state) VALUES (?, ?, ?, ?, datetime(), 0)", (part_name, session["user_id"], price, description))
    
    # Compatibility 
    compatibilities = part["compatibility"]
    for row in compatibilities:
        idcarmake = row["id_car_make"]
        idcarmodel = row["id_car_model"]
        idyear = row["id_year"]
        db.execute("INSERT INTO part_compatibility (id_car_make, id_car_model, id_year, id_part) VALUES (?, ?, ?, ?)", (idcarmake, idcarmodel, idyear, idpart))

    # Features
    features = part["features"]
    for row in features:
        name = row["name"].upper()
        value = row["value"].upper()
        descrip = row["description"].upper()
        db.execute("INSERT INTO features (name, value, description, idpart) VALUES (?, ?, ?, ?)", (name, value, descrip, idpart))


    # pictures
    for file in request.files:
        picture = request.files.getlist(file)
        id = db.execute_returnid("INSERT INTO pictures (date, name) VALUES (datetime(),?)",[picture[0].filename])
        url = upload(picture[0], id)
        db.execute("UPDATE pictures SET url = ? WHERE id = ?",(url, id))
        db.execute("INSERT INTO part_pictures (idpicture, idpart) VALUES (?, ?)", (id, idpart))
    return jsonify(True)
    
@app.route("/myposts", methods=["GET"])
@login_required
def myposts():
    iduser = session["user_id"]
    list = db.execute("SELECT id, part_name, cast(price as text) price, description, date, state FROM parts WHERE id_user = ?",(iduser,))
    return render_template("myposts.html", list = list)

@app.route("/editpart", methods=["GET","POST"])    
@login_required
def editpart():
    if request.method == "GET":
        idpart = request.args.get("id")
        part = db.execute("SELECT * FROM parts WHERE id = ?",(idpart,))[0]
        cars = db.execute("SELECT * FROM car_makes")
        compatibility = db.getCompatibility(idpart)
        pictures = db.getPictures(idpart)    
        features = db.getFeatures(idpart)
        part.update({'compatibility': compatibility, 'pictures': pictures, 'cars': cars, 'features':features})       
        return render_template("editpart.html", part = part)
    else:
        idpart = request.form.get("part_id")
        partname = request.form.get("part_name")
        price = request.form.get("price")
        description = request.form.get("description")
        try:
            db.execute("UPDATE parts SET part_name = ?, price = ?, description = ? WHERE id = ?",(partname, price, description, idpart))
            return redirect("/myposts")
        except:
            return redirect("/error")
@app.route("/deletepicture", methods=["POST"])
@login_required
def deletepicture():
    idpicture = request.form.get("id")
    idpart = request.form.get("idpart")
    pictureinfo = db.execute("SELECT name FROM pictures WHERE id = ?",(idpicture,))[0]
    try:
        # delete picture from blobs 
        delete(pictureinfo["name"])

        # delete picture from database
        db.execute("DELETE FROM pictures WHERE id = ?", (idpicture,))
        db.execute("DELETE FROM part_pictures WHERE idpicture = ?", (idpicture,))

        # get updated pictures
        
        pictures = pictures = db.getPictures(idpart) 
        return jsonify(pictures)
    except:
        return jsonify(False)

@app.route("/uploadpicture", methods=["POST"])
@login_required
def uploadpicture():
    part = json.loads(request.form.get('object'))    
    idpart = part["idpart"]
    try:
        for file in request.files:
            picture = request.files.getlist(file)
            id = db.execute_returnid("INSERT INTO pictures (date, name) VALUES (datetime(),?)",[picture[0].filename])
            url = upload(picture[0], id)
            db.execute("UPDATE pictures SET url = ? WHERE id = ?",(url, id))
            db.execute("INSERT INTO part_pictures (idpicture, idpart) VALUES (?, ?)", (id, idpart))
        pictures = pictures = db.getPictures(idpart)
        return jsonify(pictures)
    except:
        return jsonify(False)

@app.route("/deletecompatibility", methods=["POST"])
@login_required
def deletecompatibility():
    id = request.form.get("id")
    idpart = request.form.get("idpart")
    try:
        db.execute("DELETE FROM part_compatibility WHERE id = ?",(id,))
        compatibility = db.getCompatibility(idpart)
        return jsonify(compatibility)
    except:
        return jsonify(False)

@app.route("/addcompatibility", methods=["POST"])
@login_required
def addcompatibility():
    idpart = request.form.get("idpart")
    idcarmake = request.form.get("idcarmake")
    idmodel = request.form.get("idmodel")
    idyear = request.form.get("idyear")
    try:
        db.execute("INSERT INTO part_compatibility (id_car_make, id_car_model, id_year, id_part) VALUES (?, ?, ?, ?)", (idcarmake, idmodel, idyear, idpart))
        compatibility = db.getCompatibility(idpart)
        return jsonify(compatibility)
    except:
        return jsonify(False)

@app.route("/getautocomplete")
def getautocomplete():
    list = db.execute("SELECT distinct part_name FROM parts")
    return jsonify(list)

@app.route("/deletepost", methods=["POST"])
@login_required
def deletepost():
    id = request.form.get('id')

    # delete pictures
    pictures = db.execute("SELECT pictures.name, pictures.id FROM pictures INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture WHERE part_pictures.idpart = ?", (id,))
    for picture in pictures:
        delete(picture["name"])
        db.execute("DELETE FROM pictures WHERE id = ?", (picture["id"],))
    db.execute("DELETE FROM part_pictures WHERE idpart = ?",(id,))

    # compatibility
    db.execute("DELETE FROM part_compatibility WHERE id_part = ?",(id,))

    # part
    db.execute("DELETE FROM parts WHERE id = ?",(id,))

    # finally 
    return redirect("/myposts")

@app.route("/deletefeature", methods=["POST"])
@login_required
def deletefeature():
    idfeature = request.form.get('idfeature')
    idpart = request.form.get('idpart')
    try:
        db.execute("DELETE FROM features WHERE id = ?",(idfeature,))
        features = db.getFeatures(idpart)
        return jsonify(features)
    except:
        return jsonify(False)    

@app.route("/addfeature", methods=["POST"])
@login_required
def addfeature():
    name = request.form.get('name')
    value = request.form.get('value')
    description = request.form.get('description')
    idpart = request.form.get('idpart')
    try:
        db.execute('INSERT INTO features (name, value, description, idpart) VALUES (?, ?, ?, ?)',(name, value, description, idpart))
        features = db.getFeatures(idpart)
        return jsonify(features)
    except:
        return jsonify(False)


