from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database
db = SQLAlchemy(app)
