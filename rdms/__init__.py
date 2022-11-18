from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import timedelta


# Initialize flask app
app = Flask(__name__) 

app.secret_key = '12345'

# Configure database connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/ers'
#app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://ekgqjxoxmvwrxs:1efbb0cf2bc204e2879e7fdb41725b2b7b84b0db2462c00c14b204f6a8077acb@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d5vdbp2elh8edp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=180)
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

db = SQLAlchemy(app)

student_details = {
    'test123@mu.stu.edu': ('student', False), 'test122@mu.stu.edu': ('password', False)
}

admin_details = {
    'test@mu.admin': ('admin', True)
}

from rdms.models import Users,Students

def insert_data():
    # student_details = details()[0]
    # admin_details = details()[1]

    for email, user_details in student_details.items():
        student = Users.query.filter_by(email=email).first()
        if not student:
            password = (user_details[0])
            new_student = Users(email=email, password=password, admin=user_details[1])
            db.session.add(new_student)
            db.session.commit()

    for email, user_details in admin_details.items():
        admin = Users.query.filter_by(email=email).first()
        if not admin:
            password = (user_details[0])
            new_admin = Users(email=email, password=password, admin=user_details[1])
            db.session.add(new_admin)
            db.session.commit()

    for email, user_details in student_details.items():
        student = Students.query.filter_by(email=email).first()
        if not student:
            new_student = Students(email=email)
            db.session.add(new_student)
            db.session.commit()



from rdms import routes
with app.app_context():
    db.create_all()
    insert_data()
