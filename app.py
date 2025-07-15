from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# MySQL connection (WAMP/XAMPP)
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="feedback_db"
)

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("home.html", year=datetime.now().year)


# ---------- STUDENT REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        if cur.fetchone():
            flash("Email already registered!", "warning")
            return redirect(url_for('register'))

        cur.execute("INSERT INTO students (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")


# ---------- STUDENT LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[3], password):
            session['student_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# ---------- STUDENT DASHBOARD ----------
@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    return render_template("student_dashboard.html",
                           student_name=session['name'],
                           student_email=session['email'])


# ---------- SUBMIT FEEDBACK ----------
@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        staff_name = request.form['staff_name']
        department = "CSE"  # Fixed department
        teaching = request.form['rating_teaching']
        communication = request.form['rating_communication']
        punctuality = request.form['rating_punctuality']
        comment = request.form.get('comment', '')

        cur = db.cursor()
        cur.execute("""
            INSERT INTO feedbacks 
            (student_id, staff_name, department, rating_teaching, rating_communication, rating_punctuality, comment) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session['student_id'], staff_name, department, teaching, communication, punctuality, comment))
        db.commit()

        return render_template("feedback_submitted.html")

    return render_template("submit_feedback.html")

# ---------- ADMIN LOGIN ----------
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cur.fetchone()

        if admin and password == admin[2]:  # password is plain text here
            session['admin'] = admin[1]
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid admin credentials", "danger")

    return render_template("admin_login.html")


# ---------- ADMIN VIEW FEEDBACK ----------
@app.route('/admin_view')
def admin_view():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("""
        SELECT s.name AS student_name,f.staff_name, f.rating_teaching, f.rating_communication,
               f.rating_punctuality, f.comment, f.created_at
        FROM feedbacks f
        JOIN students s ON f.student_id = s.id
        ORDER BY f.created_at DESC
    """)
    feedbacks = cur.fetchall()
    return render_template("admin_view.html", feedbacks=feedbacks)


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
