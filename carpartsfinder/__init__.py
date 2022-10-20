from flask import Flask
from flask_session import Session
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

import carpartsfinder.loginmanager, carpartsfinder.carsmanager, carpartsfinder.usersmanager, carpartsfinder.partsmanager, carpartsfinder.mainmanager
