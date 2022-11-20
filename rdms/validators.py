from email_validator import validate_email, EmailNotValidError


def validate_admin_email(admin_email):
    # Email must be properly formatted (not necessarily exist)
    # Email must not end with 'mu.stu.edu'
    try:
        if (validate_email(admin_email, check_deliverability=False)
                and admin_email.endswith('mu.stu.edu')):
            error_message = "Admin email must end only with 'mu.admin'"
            return False, error_message
    except EmailNotValidError as e:
        return False, e
    return True,


def validate_student_email(student_email):
    # Email must end with 'mu.stu.edu'
    try:
        if (validate_email(student_email, check_deliverability=False)
                and not student_email.endswith('mu.stu.edu')):
            error_message = "Student email must end with 'mu.stu.edu.'"
            return False, error_message
    except EmailNotValidError as e:
        return False, e
    return True,


def validate_course_code(course_code):
    # Course codes should be six characters long.
    # The first three characters should be uppercase letters.
    # The last three characters should be numbers
    course_code = course_code.strip()
    first_integer = -1
    for char in course_code:
        if char.isdigit():
            first_integer = int(char)
            break

    if (len(course_code) != 6
            or not (course_code[:3].isalpha()
                    and course_code[:3].isupper()) or not course_code[3:].isdigit()):
        error_message = 'Please follow the convention for adding course codes'
        return False, error_message, first_integer

    return True
    
