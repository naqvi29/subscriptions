import re
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "subscriptions"
db = client[database_name]

# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    else:
        return redirect(url_for("login"))

# login route
@app.route("/login", methods=['GET','POST'])
def login():
    if not "loggedin" in session:
        if request.method == 'POST':
            if "username" in request.form and "password" in request.form:
                username = request.form.get("username")
                password = request.form.get("password")
                # now fetch admin data from db
                query = {"username":username}
                adminData = db.admin.find_one(query)
                if adminData:
                    if password == adminData['password']:                
                        session['loggedin'] = True
                        session['id'] = str(adminData['_id'])
                        session['username'] = adminData['username']
                        session['type'] = "admin"        
                        return redirect(url_for('index'))
                    else:
                        return render_template("login.html", message = "Invalid Password!")
                else:
                    return render_template("login.html", message = "Invalid Username!")
            else:
                return render_template("login.html", message = "Missing Username or Password!")
        else:
            return render_template("login.html",message="")
    else:
        return redirect(url_for("index"))

# logout route
@app.route('/logout')
def logout():
        # Remove session data, this will log the user out 
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('type', None)
        # Redirect to index page
        return redirect(url_for('login'))

# 35 pounds subsctiptions route
@app.route("/35-pound-subscriptions")
def thirty_five_pound_substriptions():
    if 'loggedin' in session:
        data = db.thirty_five_pound.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("35pound.html",data=lists)
    else:
        return redirect(url_for("login"))

# add a new subscription route 
@app.route("/add-subscription/<string:category>")
def add_subscription(category):
    if 'loggedin' in session:
        if request.method == 'POST':
            re
        else:
            return render_template("add-subscription.html")




if __name__ == '__main__':
    app.run(debug=True)