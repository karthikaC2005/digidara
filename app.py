from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='yourpassword'
app.config['MYSQL_DB']='feedback_db'

mysql=MySQL(app)

@app.route('/')
def select_faculty():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM faculty")
    faculty_list=cur.fetchall()
    return render_template('select_faculty.html',faculty=faculty_list)
@app.route('/submit_feedback/<int:faculty_id>',methods=['GET','POST'])
def submit_feedback(faculty_id):
    if request.method=='POST':
        student_name=request.form['student_name']
        rating=request.form['rating']
        comments=request.form['comments']
        cur=mysql.connection.cursor()
        cur.execute('''INSERT INTO feedback (faculty_id,student_name,rating,comments) VALUES (%s,%s,%s,%s)''',(faculty_id,student_name,rating,comments))
        mysql.connection.commit()
        return render_template('confirmation.html',name=student_name)
    return render_template('submit_feedback.html',faculty_id=faculty_id)
@app.route('/admin_feedback')
def admin_feedback():
    cur=mysql.connection.cursor()
    cur.execute('''SELECT f.name,f.department,AVG(rating) AS avg_rating,COUNT(*) AS total FROM feedback fb JOIN faculty f ON fb.aculty_id=f.faculty_id GROUP BY fb.culty_id''')
    summary=cur.fetchall()
    return render_template('admin_feedback_view.html',summary=summary)


        