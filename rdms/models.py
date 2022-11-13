from flask import abort, flash, request, render_template
from flask_login import LoginManager, UserMixin, current_user

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

from rdms.validators import validate_student_email, validate_admin_email 
from rdms.validators import validate_course_code

from rdms import app, db


# Initialize flask admin app with bootstrap4 template 
admin = Admin(app, name='Admin Page', template_mode='bootstrap4')

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# user_loader callback function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Handle unauthorized requests to admin page from users
@app.errorhandler(403)
def not_found_error(error):
    return render_template('403.html')


# Handle page not found error (404)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')  


class Users(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # password = db.Column(db.String(1000),
    #                      default=generate_password_hash('1234'))
    password = db.Column(db.String(1000),
                         default='1234')
    admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f'{self.email}'


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile = db.relationship('Profiles', backref='student_email', 
                              uselist=False)

    def __repr__(self) -> str:
        return f'{self.email}'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), db.ForeignKey('students.email'), 
                      nullable=False, unique=True)
    faculty = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    currentClass = db.Column(db.Integer, nullable=False)
    subjects = db.Column(db.String(100),nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    nationality = db.Column(db.String(100), nullable=False, default='Indian')
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow, 
                             onupdate=datetime.utcnow)
    student_details = db.relationship('Results', backref='student_detail')

    def __repr__(self) -> str:
        return f'{self.email} {self.currentClass} {self.department}'
    
# class Subject(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     currentClass = db.Column(db.Integer,nullable=False)
#     subjects = db.Column(db.String(100),nullable=False)
#     subjectCode = db.Column(db.String(50),db.ForeignKey('profiles.code'), nullable=False,unique=True)
#
#     def __repr__(self) -> str:
#         return f'{self.subjects}'


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey('profiles.email'), 
                      nullable=False)
    code = db.Column(db.String(50), nullable=False,)
    description = db.Column(db.String(200), nullable=False)
    result = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'{self.email}'


class CourseView(BaseView):
    """Extend BaseView class."""

    # Add new url endpoint '/admin/courses'
    @expose('/')
    def index(self):
        return self.render('courses.html')


class UsersView(ModelView):
    # if Admin can delete or edit data from 'users' table
    can_delete = True
    can_edit = True

    # Use 'admin' column as default column sort 
    column_default_sort = ('admin', False)
    column_searchable_list = ['email']
    # Make 'password' field read only.
    form_widget_args = {
        'password': {
            'readonly': True
        }
    }

    # Admins only can access this page
    def is_accessible(self):
        if current_user.is_authenticated and current_user.admin == True:
            return current_user.is_authenticated
        else:
            return abort(403) 

    def validate_form(self, form):
        try:
            # Admin email validation
            # User must be an admin and validate only on form submit
            if form.admin.data == True and form.email.data != None:
                admin_validations = validate_admin_email(form.email.data)
                if not admin_validations[0]:
                    flash(f'{admin_validations[1]}', 'error')
                    return False
            # User must be a Student and validate only on form submit
            elif form.admin.data == False and form.email.data != None:
                student_validations = validate_student_email(form.email.data)
                if not student_validations[0]:
                    flash(f'{student_validations[1]}', 'error')
                    return False
            return super(UsersView, self).validate_form(form)
        except AttributeError:
            return super(UsersView, self).validate_form(form)

    def after_model_change(self, form, model, is_created):
        newly_added_email = model.email
        # Check if email is a student email
        if newly_added_email.endswith('mu.stu.edu'):
            # add email to students table
            new_student = Students(email=newly_added_email)
            print(new_student)
            db.session.add(new_student)
            db.session.commit() 


class ProfileView(ModelView):
    can_delete = True
    column_searchable_list = ['name', 'email']

    form_excluded_columns = 'student_details'

    # Make 'email and 'last_updated' field readonly
    form_widget_args = {
        'student_email': {
            'readonly': True
        },
        'last_updated': {
            'readonly': True
        },
    }

    # Restrict 'sex' and 'currentClass' field input data
    form_choices = {
            'sex': [
                ('Male', 'Male'), 
                ('Female', 'Female')
            ],

            'currentClass': [
            (1, 'class 1'),
            (2, 'class 2'),
            (3, 'class 3'),
            (4, 'class 4'),
            (5, 'class 5'),
            (6, 'class 6'),
            (7, 'class 7'),
            (8, 'class 8'),
            (9, 'class 9'),
            (10,'class 10')
            ],

            'subjects': [
                ('mathematics', 'Mathematics'),
                ('gk', 'General Knowledge'),
                ('socialScience', 'Social Science'),
                ('English','English'),
                ('Drawing','Drawing'),
                ('Computer','Computer'),
                ('History','History'),
                ('Geography','Geography'),
                ('Economics','Economics'),
                ('Algebra','Algebra'),
                ('Geometry','Geometry'),
                ('Political Science','Political Science'),
                ('Physical Education','Physical Education'),


            ]

        }

    def validate_form(self, form):
        # get student email from submitted form

        form_email = str(list(form.data.values())[-1])
        # validate only on submit 
        if (request.method == "POST" and 
            # Ignore Validation on edit form request
            'edit' not in request.url and
            # email must be unique i.e. a profile info per student 
            Profiles.query.filter_by(email=form_email).first()):
            flash(f'Student profile already exists for {form_email}', 'error')
            return False
        return super(ProfileView, self).validate_form(form)


class ResultView(ModelView):
    can_delete = False

    # Use email column as default column sort 
    column_default_sort = ('email', False)

    def validate_form(self, form):
        try:
            # validate only on form submit
            if form.result.data != None:
                # validate course code
                code_validations = validate_course_code(form.code.data) 
                # extract student details from submitted form
                student_detail = list(form.data.values())[-1]
                # flash error message if course code format validation fails
                if not code_validations[0]:
                    flash(f'{code_validations[1]}', 'error')
                    return False

                if form.result.data > 100 or form.result.data < 0:
                    flash('Result cannot be greater than 100 \
                        nor less than 0 😐', 'error')
                    return False
            return super(ResultView, self).validate_form(form)
        except AttributeError:
            return super(ResultView, self).validate_form(form)


class StudentView(ModelView):
    can_delete = True
    can_edit = True
    can_create = False

# class SubjectView(ModelView):
#     can_delete=True
#     can_edit = True
#     can_create = True


# Add modelview for managing database models
admin.add_view(UsersView(Users, db.session, 
               menu_icon_type='fa', menu_icon_value='fa-users'))
# admin.add_view(StudentView(Students, db.session,
#                menu_icon_type='fa', menu_icon_value='fa-list'))
admin.add_view(ProfileView(Profiles, db.session, 
               menu_icon_type='fa', menu_icon_value='fa-pencil'))
# admin.add_view(SubjectView(Subject,db.session,
#                            menu_icon_type='fa',menu_icon_value='fa-list'))
admin.add_view(ResultView(Results, db.session, 
               menu_icon_type='fa', menu_icon_value='fa-book'))
admin.add_view(CourseView(name='Courses', endpoint='courses', 
               menu_icon_type='fa', menu_icon_value='fa-database'))
