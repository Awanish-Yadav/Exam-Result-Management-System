from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta


# Initialize flask app
app = Flask(__name__) 

app.secret_key = '*****'

# Configure database connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/ers'
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://ekgqjxoxmvwrxs:1efbb0cf2bc204e2879e7fdb41725b2b7b84b0db2462c00c14b204f6a8077acb@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d5vdbp2elh8edp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=180)
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

db = SQLAlchemy(app)


from rdms import routes
with app.app_context():
    db.create_all()
