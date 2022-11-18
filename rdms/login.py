# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.secret_key = '12345'
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://ekgqjxoxmvwrxs:1efbb0cf2bc204e2879e7fdb41725b2b7b84b0db2462c00c14b204f6a8077acb@ec2-52-1-17-228.compute-1.amazonaws.com:5432/d5vdbp2elh8edp'
#
# db = SQLAlchemy(app)
#
# student_details = {
#     'test123@mu.stu.edu': ('student', True), 'test122@mu.stu.edu': ('password', True)
# }
#
# admin_details = {
#     'admin@mu.admin': ('admin', True), 'test122@mu.admin': ('password', True)
# }
#
#
# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     password = db.Column(db.String(1000))
#     admin = db.Column(db.Boolean)
#
#
# class Students(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#
# def insert_data():
#     # student_details = details()[0]
#     # admin_details = details()[1]
#
#     for email, user_details in student_details.items():
#         student = Users.query.filter_by(email=email).first()
#         if not student:
#             password = (user_details[0])
#             new_student = Users(email=email, password=password, admin=user_details[1])
#             db.session.add(new_student)
#             db.session.commit()
#
#     for email, user_details in admin_details.items():
#         admin = Users.query.filter_by(email=email).first()
#         if not admin:
#             password = (user_details[0])
#             new_admin = Users(email=email, password=password, admin=user_details[1])
#             db.session.add(new_admin)
#             db.session.commit()
#
#     for email, user_details in student_details.items():
#         student = Students.query.filter_by(email=email).first()
#         if not student:
#             new_student = Students(email=email)
#             db.session.add(new_student)
#             db.session.commit()
#
#
#
# if __name__ == '__main__':
#     with app.app_context():
#         insert_data()
