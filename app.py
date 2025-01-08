from flask import Flask
from flask_cors import CORS
from config import Config
from flask_mysqldb import MySQL
from routes import init_routes

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Configuration de la base de données MySQL
mysql = MySQL(app)

# Activation de CORS
CORS(app)

# Initialisation des routes
init_routes(app, mysql)

if __name__ == '__main__':
    app.run(debug=True)
