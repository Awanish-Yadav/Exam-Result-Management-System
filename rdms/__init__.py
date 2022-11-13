from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta


# Initialize flask app
app = Flask(__name__) 

app.secret_key = '12345'
DB_NAME = "database.db"

# Configure database connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/ers'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=180)
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

db = SQLAlchemy(app)


from rdms import routes
with app.app_context():
    db.create_all()
