from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

app=Flask(__name__)

db=mysql.connector.connect(
host="localhost",
user="root",
password="",
database="app"
)
cursor=db.cursor()

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/select_faculty')
def select_facult():
   return render_template('select_faculty.html')        
@app.route('/submit',methods=['POST'])
def submit():
       faculty=request.form['faculty']
       student_name=request.form['student_name']
       rating=request.form['rating']
       comments=request.form['comments']
       insert_query='''INSERT INTO facult (faculty,student_name,rating,comments) VALUES (%s,%s,%s,%s)'''
       cursor.execute(insert_query,(faculty,student_name,rating,comments))
       db.commit()
       return render_template('confirmation.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')
@app.route('/home')
def index():
    return render_template('home.html')
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    error= None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Connect to the database
        #db=mysql.connector.connect(
        #host="localhost",
        #user="root",
        #password="",
        #database="app"
        #)
        cursor=db.cursor()
        cursor.execute('''SELECT * FROM admine WHERE username=%s AND password=%s''', (username, password))
        result = cursor.fetchone()
        
        if result:
            return redirect(url_for('admin_feedback_view'))
        else:
            error = 'Invalid username or password'
    return render_template('admin_login.html', error=error)
            
@app.route('/admin_feedback_view')
def admin_feedback_view():
     
   # db=mysql.connector.connect(
   # host="localhost",
   # user="root",
   # password="",
   # database="app"
   # )
   # cursor=db.cursor()
   
   cursor.execute('''SELECT faculty,student_name,rating,comments FROM facult''')
   data=cursor.fetchall()


   feedback_data=[]
   for row in data:
        feedback_data.append({'Faculty':row[0],'Student_name':row[1],'Rating':row[2],'Comments':row[3]})
   return render_template('admin_feedback_view.html',feedbacks=feedback_data)


if(__name__)=='__main__':
 app.run(debug=True)



        