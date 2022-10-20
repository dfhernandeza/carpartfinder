from carpartsfinder import app
from carpartsfinder.helpers import apology, login_master_required, login_required, SQL
import json
from msilib.schema import Error
import re
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
import sqlite3
import urllib
from werkzeug.security import check_password_hash, generate_password_hash

# Initialize sql class
db = SQL("database.db")

@app.route("/")
def index():    
    cars = db.execute("SELECT * FROM car_makes")
    return render_template("index.html", cars = cars)

@app.route("/search")
def search():
    query = request.args.get("q")
    idmake = request.args.get("make")
    idmodel = request.args.get("model")
    idyear = request.args.get("year")
    cars = db.execute("SELECT * FROM car_makes")
    if not idmake:
        q = "%" + query + "%"
        list = db.execute("""SELECT parts.id, parts.part_name, parts.date, parts.price, parts.description, 
                            users.first_name, users.last_name, users.address, cast(users.id as text) iduser 
                            FROM parts 
                            inner join users on parts.id_user = users.id
                            WHERE parts.part_name like ? and parts.state = 0""",[q])
        
        for item in list:
            compatibility = db.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year
                                          FROM car_makes 
                                          INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                                          INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                                          INNER JOIN years on years.id = part_compatibility.id_year 
                                          WHERE part_compatibility.id_part = ? """,[item["id"]])
            pictures = db.execute("""SELECT pictures.url, pictures.name FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""",[item["id"]])
            address = urllib.parse.quote(item['address'], safe='')
            item.update({'compatibility': compatibility, 'pictures': pictures, 'urladdress':address })

        return render_template("search.html", results = list, cars = cars, q = query)
    elif query and idmake and not idmodel:
        q = "%" + query + "%"
        cars = db.execute("SELECT cast(id as text) id, make FROM car_makes")
        models = db.execute("SELECT cast(id as text) id, car_model model FROM car_models WHERE car_make_id = ?",(idmake,))
        list = db.execute("""SELECT distinct parts.id, parts.part_name, parts.date, parts.price, parts.description, 
                            users.first_name, users.last_name, users.address, cast(users.id as text) iduser 
                            FROM parts 
                            inner join users on parts.id_user = users.id
                            INNER JOIN part_compatibility on parts.id = part_compatibility.id_part
                            WHERE parts.part_name like ? and part_compatibility.id_car_make = ?""",(q, idmake))
        for item in list:
            compatibility = db.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year
                                          FROM car_makes 
                                          INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                                          INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                                          INNER JOIN years on years.id = part_compatibility.id_year 
                                          WHERE part_compatibility.id_part = ? """,[item["id"]])
            pictures = db.execute("""SELECT pictures.url, pictures.name FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""",[item["id"]])
            address = urllib.parse.quote(item['address'], safe='')
            item.update({'compatibility': compatibility, 'pictures': pictures, 'urladdress':address })
        return render_template("search.html", results = list, cars = cars, q = query, idmake = idmake, models = models)
    elif query and idmake and idmodel and not idyear:
        q = "%" + query + "%"
        cars = db.execute("SELECT cast(id as text) id, make FROM car_makes")
        models = db.execute("SELECT cast(id as text) id, car_model model FROM car_models WHERE car_make_id = ?",(idmake,))
        years = db.execute("SELECT model_year.id_year id, years.year text FROM model_year INNER JOIN years on model_year.id_year = years.id WHERE model_year.id_model = ?",(idmodel,))
        list = db.execute("""SELECT distinct parts.id, parts.part_name, parts.date, parts.price, parts.description, 
                            users.first_name, users.last_name, users.address, cast(users.id as text) iduser 
                            FROM parts 
                            inner join users on parts.id_user = users.id
                            INNER JOIN part_compatibility on parts.id = part_compatibility.id_part
                            WHERE parts.part_name like ? and part_compatibility.id_car_make = ? and part_compatibility.id_car_model = ?""",(q, idmake, idmodel))
        for item in list:
            compatibility = db.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year
                                          FROM car_makes 
                                          INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                                          INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                                          INNER JOIN years on years.id = part_compatibility.id_year 
                                          WHERE part_compatibility.id_part = ? """,[item["id"]])
            pictures = db.execute("""SELECT pictures.url, pictures.name FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""",[item["id"]])
            address = urllib.parse.quote(item['address'], safe='')
            item.update({'compatibility': compatibility, 'pictures': pictures, 'urladdress':address })
        return render_template("search.html", results = list, cars = cars, q = query, idmake = idmake, idmodel = idmodel, models = models, years = years)
    elif query and idmake and idmodel and idyear:
        q = "%" + query + "%"
        cars = db.execute("SELECT cast(id as text) id, make FROM car_makes")
        models = db.execute("SELECT cast(id as text) id, car_model model FROM car_models WHERE car_make_id = ?",(idmake,))
        years = db.execute("SELECT cast(model_year.id_year as text) id, years.year text FROM model_year INNER JOIN years on model_year.id_year = years.id WHERE model_year.id_model = ?",(idmodel,))
        list = db.execute("""SELECT distinct parts.id, parts.part_name, parts.date, parts.price, parts.description, 
                            users.first_name, users.last_name, users.address, cast(users.id as text) iduser 
                            FROM parts 
                            inner join users on parts.id_user = users.id
                            INNER JOIN part_compatibility on parts.id = part_compatibility.id_part
                            WHERE parts.part_name like ? and part_compatibility.id_car_make = ? and part_compatibility.id_car_model = ? and part_compatibility.id_year = ?""",(q, idmake, idmodel, idyear))
        for item in list:
            compatibility = db.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year
                                          FROM car_makes 
                                          INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                                          INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                                          INNER JOIN years on years.id = part_compatibility.id_year 
                                          WHERE part_compatibility.id_part = ? """,[item["id"]])
            pictures = db.execute("""SELECT pictures.url, pictures.name FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""",[item["id"]])
            address = urllib.parse.quote(item['address'], safe='')
            item.update({'compatibility': compatibility, 'pictures': pictures, 'urladdress':address })
        return render_template("search.html", results = list, cars = cars, q = query, idmake = idmake, idmodel = idmodel, models = models, years = years, idyear = idyear)

@app.route("/sellerinfo")
def sellerinfo():
   iduser = request.args.get('id')
   if not iduser:
       return redirect("/")
   else:
       userinfo = db.execute("SELECT * FROM users WHERE id = ?",(iduser,))[0]
       useritems = db.execute("""SELECT parts.id, parts.part_name, parts.date, parts.price, parts.description 
                                    FROM parts 
                                    inner join users on parts.id_user = users.id
                                    WHERE users.id = ? and parts.state = 0""", (iduser,))
       for item in useritems:
           pictures = db.execute("""SELECT pictures.url, pictures.name FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""",[item["id"]])
           compatibility = db.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year
                                          FROM car_makes 
                                          INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                                          INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                                          INNER JOIN years on years.id = part_compatibility.id_year 
                                          WHERE part_compatibility.id_part = ? """,[item["id"]])
           item.update({'compatibility': compatibility, 'pictures': pictures})
       userinfo.update({'useritems':useritems})
       return render_template("userinfo.html", userinfo = userinfo) 

@app.route("/partdetails")
def partdetails():
      idpart = request.args.get("id")
      part = db.execute("SELECT * FROM parts WHERE id = ?",(idpart,))[0]
      compatibility = db.getCompatibility(idpart)
      pictures = db.getPictures(idpart)    
      features = db.getFeatures(idpart)
      sellerinfo = db.getSeller(idpart)[0]
      part.update({'compatibility': compatibility, 'pictures': pictures, 'features':features, 'sellerinfo':sellerinfo})       
      return render_template("partdetails.html", part = part)
                               