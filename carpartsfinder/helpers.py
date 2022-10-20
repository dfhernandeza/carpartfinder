import os
import urllib.parse
import sqlite3
from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, header, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=message, header = header)

def login_master_required(f):
    """
    Decorate routes to require master rol.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_rol") != "master":
            return apology("You don't have permission to access this resource.","Forbidden", 403)
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def dict_factory(cursor, row):
    """returns dictionay"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SQL():
    """Class to handle database connection"""
    def __init__(self, name):
        self.name = name
    
    def execute(self, query, params = None):
        """Returns a list of rows from database"""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        data = [] 
        if params == None:
            data = cur.execute(query).fetchall()            
        else:
            data = cur.execute(query, params).fetchall()
            db.commit()                  
        db.close()
        return data
    
    def execute_returnid(self, query, params = None):
        """Inserts row to database and returns the id of the inserted item."""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        cur.execute(query, params)
        db.commit()
        data = cur.lastrowid                  
        db.close()
        return data 

    def getCompatibility(self, idpart):
        """Returns compatibility provided a part id"""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        data =  cur.execute("""SELECT car_makes.make, car_models.car_model, cast(years.year as text) year, part_compatibility.id, part_compatibility.id_car_make, part_compatibility.id_car_model, part_compatibility.id_year, part_compatibility.id_part
                               FROM car_makes 
                               INNER JOIN part_compatibility on car_makes.id = part_compatibility.id_car_make
                               INNER JOIN car_models on car_models.id = part_compatibility.id_car_model
                               INNER JOIN years on years.id = part_compatibility.id_year 
                               WHERE part_compatibility.id_part = ? """,(idpart,)).fetchall()          
        db.close()
        return data

    def getPictures(self, idpart):
        """Return a list of pictures provided a part id"""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        data =  cur.execute("""SELECT pictures.url, pictures.name, part_pictures.idpicture id FROM pictures 
                                     INNER JOIN part_pictures ON pictures.id = part_pictures.idpicture 
                                     WHERE part_pictures.idpart = ?""", (idpart,)).fetchall()                    
        db.close()
        return data

    def getFeatures(self, idpart):
        """Return a list of features provided a part id"""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        data =  cur.execute("""SELECT name, value, description, id FROM features WHERE idpart = ?""", (idpart,)).fetchall()                    
        db.close()
        return data

    def getSeller(self, idpart):
        """Return the seller provided a part id"""
        db = sqlite3.connect(self.name)
        db.row_factory = dict_factory        
        cur = db.cursor()
        data =  cur.execute("""SELECT email, first_name, last_name, phone_number, address, cast(users.id as text) id FROM users INNER JOIN parts on users.id = parts.id_user WHERE parts.id = ?""", (idpart,)).fetchall()                    
        db.close()
        return data
