import sqlite3
def create_database():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin')),
            profile TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            description TEXT,
            fee REAL,
            schedule TEXT,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES users(user_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            status TEXT NOT NULL CHECK(status IN ('enrolled', 'completed', 'dropped')),
            grade REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            amount REAL,
            payment_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role, profile):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, role, profile)
        VALUES (?, ?, ?, ?)
    ''', (username, password, role, profile))
    conn.commit()
    conn.close()

def login(username, password):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def user_menu(role):
    if role == 'login':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login(username, password)
        if user:
            user_id, _, role, _ = user
            if role == 'admin':
                admin_menu(user_id)
            elif role == 'student':
                student_menu(user_id)
            elif role == 'teacher':
                teacher_menu(user_id)
            else:
                print("Invalid role.")
        else:
            print("Invalid username or password.")
    elif role == 'register':
        # اضافه کردن کاربر جدید
        # این قسمت را باید خودتان پیاده‌سازی کنید
        pass
    else:
        print("Invalid role. Please choose 'login' or 'register'.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)
create_database()
user_authentication()
def admin_menu(user_id):
    if user_id:
        if is_admin(user_id):
            print("Welcome, Admin!")
            print("1. Add Course")
            print("2. View Course Report")
            choice = input("Enter your choice: ")
            if choice == '1':
                add_course_by_admin(user_id)
            elif choice == '2':
                course_report = get_course_report()
                print("Course Report:")
                for course in course_report:
                    print(course)
            else:
                print("Invalid choice.")
        else:
            print("You are not authorized to access this menu.")
    else:
        print("Invalid username or password.")

def add_course_by_admin(admin_id):
    if is_admin(admin_id):
        course_name = input("Enter course name: ")
        description = input("Enter course description: ")
        fee = float(input("Enter course fee: "))
        schedule = input("Enter course schedule: ")
        teacher_id = int(input("Enter teacher's user ID: "))
        add_course(course_name, description, fee, schedule, teacher_id)
        print(f"Course '{course_name}' added successfully.")
    else:
        print("You are not authorized to add courses.")

def get_course_report():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, COUNT(enrollments.user_id) as num_students, SUM(payments.amount) as total_revenue
        FROM courses
        LEFT JOIN enrollments ON courses.course_id = enrollments.course_id
        LEFT JOIN payments ON courses.course_id = payments.course_id
        GROUP BY courses.course_id
    ''')
    report = c.fetchall()
    conn.close()
    return report

def is_admin(user_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
    role = c.fetchone()[0]
    conn.close()
    return role == 'admin'

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)
create_database()
user_authentication()

def teacher_menu(teacher_id):
    if teacher_id:
        print("Welcome, Teacher!")
        print("1. View My Courses")
        print("2. Update Attendance and Grades")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_teacher_courses(teacher_id)
        elif choice == '2':
            update_attendance_and_grades(teacher_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

def view_teacher_courses(teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE teacher_id = ?', (teacher_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your courses:")
        for course in courses:
            print(course)
    else:
        print("You are not assigned to any courses.")

def update_attendance_and_grades(teacher_id):
    course_id = int(input("Enter course ID: "))
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ? AND teacher_id = ?', (course_id, teacher_id))
    course = c.fetchone()
    if course:
        # اگر استاد به دوره مربوطه تعلق داشته باشد
        # این قسمت را باید خودتان پیاده‌سازی کنید
        print("Attendance and grades updated successfully.")
    else:
        print("You are not assigned to this course.")
    conn.close()

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)
create_database()
user_authentication()

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role (student/teacher/admin): ")
    profile = input("Enter your profile details: ")
    add_user(username, password, role, profile)
    print("User registered successfully.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    if role_input == 'login':
        user_menu('login')
    elif role_input == 'register':
        register_user()
    else:
        print("Invalid input.")
create_database()
user_authentication()

def add_course(course_name, description, fee, schedule, teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO courses (course_name, description, fee, schedule, teacher_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (course_name, description, fee, schedule, teacher_id))
    conn.commit()
    conn.close()

def view_teacher_courses(teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE teacher_id = ?', (teacher_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your courses:")
        for course in courses:
            print(course)
    else:
        print("You are not assigned to any courses.")

def update_attendance_and_grades(teacher_id):
    course_id = int(input("Enter course ID: "))
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ? AND teacher_id = ?', (course_id, teacher_id))
    course = c.fetchone()
    if course:
        # اگر استاد به دوره مربوطه تعلق داشته باشد
        # این قسمت را باید خودتان پیاده‌سازی کنید
        print("Attendance and grades updated successfully.")
    else:
        print("You are not assigned to this course.")
    conn.close()

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)
create_database()
user_authentication()

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role (student/teacher/admin): ")
    profile = input("Enter your profile details: ")
    add_user(username, password, role, profile)
    print("User registered successfully.")

def login(username, password):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def user_menu(role):
    if role == 'login':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login(username, password)
        if user:
            user_id, _, role, _ = user
            if role == 'admin':
                admin_menu(user_id)
            elif role == 'student':
                student_menu(user_id)
            elif role == 'teacher':
                teacher_menu(user_id)
            else:
                print("Invalid role.")
        else:
            print("Invalid username or password.")
    elif role == 'register':
        register_user()
    else:
        print("Invalid role. Please choose 'login' or 'register'.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()

def admin_menu(user_id):
    if user_id:
        if is_admin(user_id):
            print("Welcome, Admin!")
            print("1. Add Course")
            print("2. View Course Report")
            choice = input("Enter your choice: ")
            if choice == '1':
                add_course_by_admin(user_id)
            elif choice == '2':
                course_report = get_course_report()
                print("Course Report:")
                for course in course_report:
                    print(course)
            else:
                print("Invalid choice.")
        else:
            print("You are not authorized to access this menu.")
    else:
        print("Invalid username or password.")

def add_course_by_admin(admin_id):
    if is_admin(admin_id):
        course_name = input("Enter course name: ")
        description = input("Enter course description: ")
        fee = float(input("Enter course fee: "))
        schedule = input("Enter course schedule: ")
        teacher_id = int(input("Enter teacher's user ID: "))
        add_course(course_name, description, fee, schedule, teacher_id)
        print(f"Course '{course_name}' added successfully.")
    else:
        print("You are not authorized to add courses.")

def get_course_report():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, COUNT(enrollments.user_id) as num_students, SUM(payments.amount) as total_revenue
        FROM courses
        LEFT JOIN enrollments ON courses.course_id = enrollments.course_id
        LEFT JOIN payments ON courses.course_id = payments.course_id
        GROUP BY courses.course_id
    ''')
    report = c.fetchall()
    conn.close()
    return report

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()
def teacher_menu(teacher_id):
    if teacher_id:
        print("Welcome, Teacher!")
        print("1. View My Courses")
        print("2. Update Attendance and Grades")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_teacher_courses(teacher_id)
        elif choice == '2':
            update_attendance_and_grades(teacher_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

def view_teacher_courses(teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE teacher_id = ?', (teacher_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your courses:")
        for course in courses:
            print(course)
    else:
        print("You are not assigned to any courses.")

def update_attendance_and_grades(teacher_id):
    course_id = int(input("Enter course ID: "))
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ? AND teacher_id = ?', (course_id, teacher_id))
    course = c.fetchone()
    if course:
        # اگر استاد به دوره مربوطه تعلق داشته باشد
        # این قسمت را باید خودتان پیاده‌سازی کنید
        print("Attendance and grades updated successfully.")
    else:
        print("You are not assigned to this course.")
    conn.close()

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()
def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role (student/teacher/admin): ")
    profile = input("Enter your profile details: ")
    add_user(username, password, role, profile)
    print("User registered successfully.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    if role_input == 'login':
        user_menu('login')
    elif role_input == 'register':
        register_user()
    else:
        print("Invalid input.")

create_database()
user_authentication()
def add_user(username, password, role, profile):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role, profile) VALUES (?, ?, ?, ?)', (username, password, role, profile))
    conn.commit()
    conn.close()

def add_course(course_name, description, fee, schedule, teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO courses (course_name, description, fee, schedule, teacher_id) VALUES (?, ?, ?, ?, ?)', (course_name, description, fee, schedule, teacher_id))
    conn.commit()
    conn.close()

def get_course_report():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, COUNT(enrollments.user_id) as num_students, SUM(payments.amount) as total_revenue
        FROM courses
        LEFT JOIN enrollments ON courses.course_id = enrollments.course_id
        LEFT JOIN payments ON courses.course_id = payments.course_id
        GROUP BY courses.course_id
    ''')
    report = c.fetchall()
    conn.close()
    return report

def view_courses():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Available courses:")
        for course in courses:
            print(course)
    else:
        print("No courses available.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()

def add_user(username, password, role, profile):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role, profile) VALUES (?, ?, ?, ?)', (username, password, role, profile))
    conn.commit()
    conn.close()

def add_course(course_name, description, fee, schedule, teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO courses (course_name, description, fee, schedule, teacher_id) VALUES (?, ?, ?, ?, ?)', (course_name, description, fee, schedule, teacher_id))
    conn.commit()
    conn.close()

def get_course_report():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, COUNT(enrollments.user_id) as num_students, SUM(payments.amount) as total_revenue
        FROM courses
        LEFT JOIN enrollments ON courses.course_id = enrollments.course_id
        LEFT JOIN payments ON courses.course_id = payments.course_id
        GROUP BY courses.course_id
    ''')
    report = c.fetchall()
    conn.close()
    return report

def view_courses():
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Available courses:")
        for course in courses:
            print(course)
    else:
        print("No courses available.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()

def enroll_in_course(user_id, course_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', (user_id, course_id))
    conn.commit()
    conn.close()

def pay_for_course(user_id, course_id, amount):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('INSERT INTO payments (user_id, course_id, amount) VALUES (?, ?, ?)', (user_id, course_id, amount))
    conn.commit()
    conn.close()

def student_menu(student_id):
    if student_id:
        print("Welcome, Student!")
        print("1. View Available Courses")
        print("2. Enroll in Course")
        print("3. View Enrolled Courses")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_courses()
        elif choice == '2':
            course_id = int(input("Enter course ID to enroll: "))
            enroll_in_course(student_id, course_id)
            amount = float(input("Enter payment amount: "))
            pay_for_course(student_id, course_id, amount)
            print(f"Enrolled in course {course_id} and paid {amount}.")
        elif choice == '3':
            view_enrolled_courses(student_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

def view_enrolled_courses(student_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, courses.description, courses.schedule, courses.fee
        FROM courses
        JOIN enrollments ON courses.course_id = enrollments.course_id
        WHERE enrollments.user_id = ?
    ''', (student_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your enrolled courses:")
        for course in courses:
            print(course)
    else:
        print("You are not enrolled in any courses.")

def is_admin(user_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
    role = c.fetchone()
    conn.close()
    return role[0] == 'admin'

def login(username, password):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def user_menu(role):
    if role == 'login':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login(username, password)
        if user:
            user_id, _, role, _ = user
            if role == 'admin':
                admin_menu(user_id)
            elif role == 'student':
                student_menu(user_id)
            elif role == 'teacher':
                teacher_menu(user_id)
            else:
                print("Invalid role.")
        else:
            print("Invalid username or password.")
    elif role == 'register':
        register_user()
    else:
        print("Invalid role. Please choose 'login' or 'register'.")

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role (student/teacher/admin): ")
    profile = input("Enter your profile details: ")
    add_user(username, password, role, profile)
    print("User registered successfully.")

create_database()
user_authentication()

def add_course_by_admin(admin_id):
    if is_admin(admin_id):
        course_name = input("Enter course name: ")
        description = input("Enter course description: ")
        fee = float(input("Enter course fee: "))
        schedule = input("Enter course schedule: ")
        teacher_id = int(input("Enter teacher's user ID: "))
        add_course(course_name, description, fee, schedule, teacher_id)
        print(f"Course '{course_name}' added successfully.")
    else:
        print("You are not authorized to add courses.")

def admin_menu(user_id):
    if user_id:
        if is_admin(user_id):
            print("Welcome, Admin!")
            print("1. Add Course")
            print("2. View Course Report")
            choice = input("Enter your choice: ")
            if choice == '1':
                add_course_by_admin(user_id)
            elif choice == '2':
                course_report = get_course_report()
                print("Course Report:")
                for course in course_report:
                    print(course)
            else:
                print("Invalid choice.")
        else:
            print("You are not authorized to access this menu.")
    else:
        print("Invalid username or password.")

def update_attendance_and_grades(teacher_id):
    course_id = int(input("Enter course ID: "))
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ? AND teacher_id = ?', (course_id, teacher_id))
    course = c.fetchone()
    if course:
        student_id = int(input("Enter student ID: "))
        attendance = input("Enter attendance status (present/absent): ")
        grade = input("Enter grade: ")
        c.execute('''
            INSERT INTO grades (course_id, student_id, attendance, grade)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(course_id, student_id) DO UPDATE SET attendance=excluded.attendance, grade=excluded.grade
        ''', (course_id, student_id, attendance, grade))
        conn.commit()
        print("Attendance and grades updated successfully.")
    else:
        print("You are not assigned to this course.")
    conn.close()

def teacher_menu(teacher_id):
    if teacher_id:
        print("Welcome, Teacher!")
        print("1. View My Courses")
        print("2. Update Attendance and Grades")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_teacher_courses(teacher_id)
        elif choice == '2':
            update_attendance_and_grades(teacher_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

create_database()
user_authentication()

def update_attendance_and_grades(teacher_id):
    course_id = int(input("Enter course ID: "))
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE course_id = ? AND teacher_id = ?', (course_id, teacher_id))
    course = c.fetchone()
    if course:
        student_id = int(input("Enter student ID: "))
        attendance = input("Enter attendance status (present/absent): ")
        grade = input("Enter grade: ")
        c.execute('''
            INSERT INTO grades (course_id, student_id, attendance, grade)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(course_id, student_id) DO UPDATE SET attendance=excluded.attendance, grade=excluded.grade
        ''', (course_id, student_id, attendance, grade))
        conn.commit()
        print("Attendance and grades updated successfully.")
    else:
        print("You are not assigned to this course.")
    conn.close()

def view_teacher_courses(teacher_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses WHERE teacher_id = ?', (teacher_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your courses:")
        for course in courses:
            print(course)
    else:
        print("You are not assigned to any courses.")

def view_enrolled_courses(student_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('''
        SELECT courses.course_name, courses.description, courses.schedule, courses.fee
        FROM courses
        JOIN enrollments ON courses.course_id = enrollments.course_id
        WHERE enrollments.user_id = ?
    ''', (student_id,))
    courses = c.fetchall()
    conn.close()
    if courses:
        print("Your enrolled courses:")
        for course in courses:
            print(course)
    else:
        print("You are not enrolled in any courses.")

def teacher_menu(teacher_id):
    if teacher_id:
        print("Welcome, Teacher!")
        print("1. View My Courses")
        print("2. Update Attendance and Grades")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_teacher_courses(teacher_id)
        elif choice == '2':
            update_attendance_and_grades(teacher_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

def user_menu(role):
    if role == 'login':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login(username, password)
        if user:
            user_id, _, role, _ = user
            if role == 'admin':
                admin_menu(user_id)
            elif role == 'student':
                student_menu(user_id)
            elif role == 'teacher':
                teacher_menu(user_id)
            else:
                print("Invalid role.")
        else:
            print("Invalid username or password.")
    elif role == 'register':
        register_user()
    else:
        print("Invalid role. Please choose 'login' or 'register'.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)
create_database()
user_authentication()

def is_admin(user_id):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
    role = c.fetchone()
    conn.close()
    return role[0] == 'admin'

def login(username, password):
    conn = sqlite3.connect('online_school.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def user_menu(role):
    if role == 'login':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = login(username, password)
        if user:
            user_id, _, role, _ = user
            if role == 'admin':
                admin_menu(user_id)
            elif role == 'student':
                student_menu(user_id)
            elif role == 'teacher':
                teacher_menu(user_id)
            else:
                print("Invalid role.")
        else:
            print("Invalid username or password.")
    elif role == 'register':
        register_user()
    else:
        print("Invalid role. Please choose 'login' or 'register'.")

def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    role = input("Enter your role (student/teacher/admin): ")
    profile = input("Enter your profile details: ")
    add_user(username, password, role, profile)
    print("User registered successfully.")

def admin_menu(user_id):
    if user_id:
        if is_admin(user_id):
            print("Welcome, Admin!")
            print("1. Add Course")
            print("2. View Course Report")
            choice = input("Enter your choice: ")
            if choice == '1':
                add_course_by_admin(user_id)
            elif choice == '2':
                course_report = get_course_report()
                print("Course Report:")
                for course in course_report:
                    print(course)
            else:
                print("Invalid choice.")
        else:
            print("You are not authorized to access this menu.")
    else:
        print("Invalid username or password.")

def student_menu(student_id):
    if student_id:
        print("Welcome, Student!")
        print("1. View Available Courses")
        print("2. Enroll in Course")
        print("3. View Enrolled Courses")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_courses()
        elif choice == '2':
            course_id = int(input("Enter course ID to enroll: "))
            enroll_in_course(student_id, course_id)
            amount = float(input("Enter payment amount: "))
            pay_for_course(student_id, course_id, amount)
            print(f"Enrolled in course {course_id} and paid {amount}.")
        elif choice == '3':
            view_enrolled_courses(student_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")


def teacher_menu(teacher_id):
    if teacher_id:
        print("Welcome, Teacher!")
        print("1. View My Courses")
        print("2. Update Attendance and Grades")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_teacher_courses(teacher_id)
        elif choice == '2':
            update_attendance_and_grades(teacher_id)
        else:
            print("Invalid choice.")
    else:
        print("Invalid user ID.")

def user_authentication():
    role_input = input("Do you want to login or register? Enter 'login' or 'register': ")
    user_menu(role_input)

create_database()
user_authentication()