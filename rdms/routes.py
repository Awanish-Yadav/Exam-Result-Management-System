from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from flask_login import current_user

from rdms import db, app 
from rdms.models import Users 


# App home page
@app.route('/')
def index():
    return render_template('home.html')


# login validation
@app.route('/login', methods=['POST', 'GET']) 
def login():
    # Check if username and password requests exist
    if request.method == "POST":
        # assume user is student
        student_email = request.form.get('student_email')
        if student_email:
            # Query Users table against student email and password
            student_password = request.form.get('student_password')
            student = Users.query.filter_by(email=student_email).first()

            # Check if the student email is valid along with the password
            if (student and (student.password == student_password)
                    and student_email.endswith('mu.stu.edu')):
                login_user(student, remember=True)
                return redirect(url_for('result')) 
            # Display message if login details are incorrect
            else:
                flash('Invalid Student Email or Password') 
                return redirect(url_for('index')) 
        # If Boolean of 'student_email' is False then validate user as an admin
        else:
            # Query Users table against admin email and password
            admin_email = request.form.get('admin_email')
            admin_password = request.form.get('admin_password')
            admin = Users.query.filter_by(email=admin_email).first()
            # Check if admin account is valid
            if (admin and (admin.password == admin_password) and
                    admin_email.endswith('mu.admin')):
                login_user(admin, remember=True)
                return redirect(url_for('admin.index')) 
            # Display message if account details does not exist
            else:
                flash('Invalid Login Details. Retry') 
                return redirect(url_for('index')) 
    else:
        # If request method is not POST redirect to home page
        return redirect(url_for('index'))


@app.route('/about')
def about():
    # Render about.html file.
    return render_template('about.html')


@app.route('/contact')
def contact():
    # Render contact.html file.
    return render_template('contact.html')


@app.route('/details')
def details():
    # Render details.html file.
    return render_template('details.html')


@app.route('/result')
@login_required
def result():
    # Render result.html file
    user_email = current_user.email
    # Query 'profiles' table for student profile details
    profile_info = db.engine.execute(
                        f"SELECT * FROM profiles \
                        WHERE email = '{user_email}'") 
    # Query 'results' table for distinct student results
    student_result = db.engine.execute(
                        f"SELECT DISTINCT code, description, result \
                        FROM results WHERE email = '{user_email}'") 
    return render_template(
            'result.html', 
            profile_info=profile_info, 
            student_result=student_result)




@app.route('/logout')
def logout():
    """Logout user and redirect to home page"""
    logout_user()
    return redirect(url_for('index')) 
