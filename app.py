from flask import Flask, render_template
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__, template_folder='template')
CORS(app)

# My SQL Instance configurations
# Change these details to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = '34.142.43.53'
mysql.init_app(app)

@app.route('/')
def home():
    return render_template("index.html")

# This is the home / index page (How to make this our starting point???)
@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template("index.html")

# Add student
@app.route("/add", methods=['GET', 'POST']) #Add Student
def add():
    if request.method == "POST":
        name = request.form['studentName']
        email = request.form['email']
        cursor = mysql.connection.cursor() #create a connection to the SQL instance
        cursor.execute('''INSERT INTO students (studentName, email) VALUES(%s,%s)''',(name,email)) # execute
        mysql.connection.commit()
        cursor.close()
    
        return render_template("success.html")

# Delete student
@app.route("/delete", methods=['GET', 'POST']) #Delete Student
def delete():
    if request.method == "POST":
        name = request.form['studentName']
        cursor = mysql.connection.cursor() #create a connection to the SQL instance
        cursor.execute('''DELETE FROM students WHERE studentName = %s''',(name)) # execute
        mysql.connection.commit()
        cursor.close()

        return render_template("success.html")


# Change to add form html
@app.route('/addPage', methods=['GET', 'POST'])
def addPage():
    return render_template("add.html")

# Change to delete form html
@app.route('/deletePage', methods=['GET', 'POST'])
def deletePage():
    return render_template("delete.html")


@app.route("/viewPage", methods=['GET', 'POST']) #Default - Show Data
def viewPage(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    Results=[]
    for row in rv: #Format the Output Results and add to return string
        Result={}
        Result['Name']=row[0].replace('\n',' ')
        Result['Email']=row[1]
        Result['ID']=row[2]
        Results.append(Result)
    response={'Results':Results, 'count':len(Results)}

    ret=app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    
    return ret

if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080
