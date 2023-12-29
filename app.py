from flask import Flask, request, render_template,redirect, url_for
import mysql.connector as sql

app = Flask(__name__)


def database():
    
    try:
        mydb = sql.connect(
        host="",#enter your configuration
        user="",
        password="",
        database="college"
        )
        
        cursor = mydb.cursor()
        
    
    except :
        print("Error connecting to MySQL")
        mydb=sql.connect( host="",user="",password="")#enter your configuration
        cursor=mydb.cursor()
        cursor.execute("create database college")
        cursor.execute("use college")
        cursor.execute("create table student (email varchar(255),password varchar(255),name varchar(255),gender varchar(255),address varchar(255),phno bigint,course varchar(255))")
        print ("Database created successfully ")
        mydb.commit()
        raise "database error"

mydb = sql.connect(
        host="",
        user="",#enter your configuration
        password="",
        database="college"
        )
        
cursor = mydb.cursor()


#intial function
@app.route('/',methods=['POST','GET'])
def index():
    
    return render_template("index.html")

#login core functions
@app.route('/process_data', methods=['POST'])
def process_data():
    # try:
    name = request.form['name']
    password = request.form['password']
    # Insert data into the table
    global username
    username=name
    if chk_data(name,password):
        return render_template("dashdash.html")

    else:
        return "Record not found please check credentials or create new account <br><a href=\"/creata\">Create account</a>"
        
    # except:
    #     name='none'
    #     password='none'
    #     print("error")    
    #     return "Error"

@app.route("/creata")
def create():
    print("create")
    return render_template('create.html')

@app.route('/log_out', methods=['POST','GET'])
def log_out():
    try:
     del username
    except:
        pass
    return redirect("/")

@app.route("/create_account", methods=['POST'])
def creation():
    name=request.form['firstname']+" "+request.form['middlename']+" "+request.form['lastname']
    course=request.form['course']
    gender=request.form['gender']
    phno=str(request.form['phno'])
    address=request.form['address']
    email=request.form['email']
    password=request.form['password']
    phno=int(phno)
    print(name,course,gender,phno,address,email,password)
    sql=f"insert into student(email,password,name,gender,address,phno,course) values('{email}','{password}','{name}','{gender}','{address}',{phno},'{course}')"
    cursor.execute(sql)
    mydb.commit()
    del name,course,gender,phno,address,email,password
    return "account created now go back and log in again <br><a href=\"/\">Log in</a>"

def chk_data(name,password):
    cursor.execute(f"select password from student where email= '{name}' and password='{password}'")
    result=cursor.fetchone()
    if result:
        return True
    else: 
        return False
    return

def data(username):
    cursor.execute(f"select * from student where email= '{username}'")
    a=cursor.fetchall()
    print(a) 
    
    return a

#nav bar functions
@app.route("/home" ,methods=['POST','GET'])
def dashboard():
    return render_template("dashdash.html")

@app.route("/profile",methods=['POST','GET'])
def profile():
    a=data(username)
    a=a[0]
    return render_template("profile.html",name=a[2],email=a[0],gender=a[3],address=a[4],phno=a[5],course=a[6])

@app.route("/payment",methods=['POST','GET'])
def payment():
    return render_template("payment.html")

@app.route("/schedule",methods=['POST','GET'])
def schdule():    
    return render_template("schedules.html")


#courses
@app.route("/python",methods=['POST','GET'])
def python():
    return "python <a href=\"/home\" class=\"logo\">Home </a> "

@app.route("/android",methods=['POST','GET'])
def android():
    return "android <a href=\"/home\" class=\"logo\">Home </a>"

@app.route("/english",methods=['POST','GET'])
def english():
    return "english <a href=\"/home\" class=\"logo\">Home </a>"


if __name__=="__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0")
   