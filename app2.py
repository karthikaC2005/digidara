from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import smtplib
from email.message import EmailMessage
from io import BytesIO
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet


app = Flask(__name__)
app.secret_key = 'your_secret_key'


db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="feedback_db"
)



@app.route('/')
def home():
    return render_template("home.html", year=datetime.now().year)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = db.cursor()
        cur.execute("SELECT * FROM student WHERE email = %s", (email,))
        if cur.fetchone():
            flash("Email already registered!", "warning")
            return redirect(url_for('register'))

        cur.execute("INSERT INTO student (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM student WHERE email=%s", (email,))
        user = cur.fetchone()

        if user and check_password_hash(user[3], password):
            session['student_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@app.route('/student_dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    return render_template("student_dashboard.html",
                           student_name=session['name'],
                           student_email=session['email'])


@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        staff_name = request.form['staff_name']
        department = "CSE"
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

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        admin = cur.fetchone()

        if admin and password == admin[2]:
            session['admin'] = admin[1]
            return redirect(url_for('admin_view'))
        else:
            flash("Invalid admin credentials", "danger")

    return render_template("admin_login.html")


@app.route('/admin_view')
def admin_view():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute("""
        SELECT s.name AS student_name, f.staff_name, f.rating_teaching, f.rating_communication,
               f.rating_punctuality, f.comment, f.created_at
        FROM feedbacks f
        JOIN student s ON f.student_id = s.id
        ORDER BY f.created_at DESC
    """)
    feedbacks = cur.fetchall()
    return render_template("admin_view.html", feedbacks=feedbacks)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        cur = db.cursor()
        cur.execute("SELECT email FROM student WHERE name=%s", (username,))
        result = cur.fetchone()

        if result:
            email = result[0]
            otp = str(random.randint(100000, 999999))
            session['reset_username'] = username
            session['otp'] = otp
            send_otp_email(email, otp)
            flash(f"Your OTP is: {otp}", "info")  
            return redirect(url_for('verify_otp'))
        else:
            flash("Username not found", "danger")

    return render_template("forgot_password.html")


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' not in session or 'reset_username' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        action = request.form['action']

        if action == 'resend':
            cur = db.cursor()
            cur.execute("SELECT email FROM student WHERE name=%s", (session['reset_username'],))
            result = cur.fetchone()
            if result:
                new_otp = str(random.randint(100000, 999999))
                session['otp'] = new_otp
                send_otp_email(result[0], new_otp)
                flash("A new OTP has been sent to your email.", "info")
            else:
                flash("Error retrieving email. Please try again.", "danger")
            return redirect(url_for('verify_otp'))

        elif action == 'verify':
            user_otp = request.form['otp']
            new_password = request.form['new_password']

            if user_otp == session['otp']:
                hashed_password = generate_password_hash(new_password)
                cur = db.cursor()
                cur.execute("UPDATE students SET password=%s WHERE name=%s",
                            (hashed_password, session['reset_username']))
                db.commit()
                session.pop('otp')
                session.pop('reset_username')
                flash("Password reset successful!", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid OTP. Please try again.", "danger")

    return render_template("verify_otp.html")


def send_otp_email(to_email, otp):
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP for Password Reset'
    msg['From'] = 'yourappsender@gmail.com'
    msg['To'] = to_email
    msg.set_content(f"Your OTP for password reset is: {otp}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('yourappsender@gmail.com', 'your_app_password')
            smtp.send_message(msg)
    except Exception as e:
        print("Error sending OTP email:", e)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

@app.route('/export_pdf')
def export_pdf():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("""
        SELECT s.name, f.staff_name, f.rating_teaching, f.rating_communication,
               f.rating_punctuality, f.comment, f.created_at
        FROM feedbacks f
        JOIN student s ON f.student_id = s.id
        ORDER BY f.created_at DESC
    """)
    feedbacks = cur.fetchall()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph("Feedback Report", styles['Title'])
    elements.append(title)

    # Table data
    data = [['Student', 'Faculty', 'Teaching', 'Communication', 'Punctuality', 'Comment', 'Date']]
    for row in feedbacks:
        data.append([
            row[0],  # student name
            row[1],  # staff name
            row[2],  # teaching
            row[3],  # communication
            row[4],  # punctuality
            row[5],  # comment
            row[6].strftime("%Y-%m-%d %H:%M:%S")  # created_at
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3f87a6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf',
                     download_name='feedback_report_table.pdf',
                     as_attachment=True)

# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)
