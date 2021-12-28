import re
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from pymongo.message import query
import os
from flask_mail import Mail, Message
import json
from time import time

app = Flask(__name__)

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "subscriptions"
db = client[database_name]

# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# configure twillo api key for emails 
# app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'apikey'
# app.config['MAIL_PASSWORD'] = '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'
# mail = Mail(app)


# mail 
# @app.route("/ttest")
# def test():
#     msg = Message(subject='Test Email', sender='testwebtrica@gmail.com', recipients=['mali29april@gmail.com'])
#     msg.body = 'This is a test email.'
#     msg.extra_headers = {'X-SMTPAPI': json.dumps({'send_at': time() + 120})}
#     mail.send(msg)
#     return "True"


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
@app.route("/thirty_five_pound")
def thirty_five_pound():
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
# 40 pounds subsctiptions route
@app.route("/fourty_pound")
def fourty_pound():
    if 'loggedin' in session:
        data = db.fourty_pound.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("40pound.html",data=lists)
    else:
        return redirect(url_for("login"))
# 45 pounds subsctiptions route
@app.route("/fourty_five_pound")
def fourty_five_pound():
    if 'loggedin' in session:
        data = db.fourty_five_pound.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("45pound.html",data=lists)
    else:
        return redirect(url_for("login"))
# 50 pounds subsctiptions route
@app.route("/fifty_pound")
def fifty_pound():
    if 'loggedin' in session:
        data = db.fifty_pound.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("50pound.html",data=lists)
    else:
        return redirect(url_for("login"))
# 65 pounds subsctiptions route
@app.route("/sixty_five_pound")
def sixty_five_pound():
    if 'loggedin' in session:
        data = db.sixty_five_pound.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("65pound.html",data=lists)
    else:
        return redirect(url_for("login"))
# family subsctiptions route
@app.route("/family_subscriptions")
def family_subscriptions():
    if 'loggedin' in session:
        data = db.family_subscriptions.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("family_subscriptions.html",data=lists)
    else:
        return redirect(url_for("login"))

# add a new subscription route 
@app.route("/add-subscription/<string:category>", methods = ['GET','POST'])
def add_subscription(category):
    if 'loggedin' in session:
        if request.method == 'POST':
            email = request.form.get("email")
            name = request.form.get("name")
            etsy_id = request.form.get("etsy_id")
            period = request.form.get("period")
            sold_price = request.form.get("sold_price")
            new_price = request.form.get("new_price")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            renewal_date = request.form.get("renewal_date")
            payment_due = request.form.get("payment_due")

            # convert datetime from string to object 
            start_date_obj = datetime.strptime(start_date,'%Y-%m-%d').strftime('%d-%b-%Y')
            end_date_obj = datetime.strptime(end_date,'%Y-%m-%d').strftime('%d-%b-%Y')
            renewal_date_obj = datetime.strptime(renewal_date,'%Y-%m-%d').strftime('%d-%b-%Y')
            payment_due_obj = datetime.strptime(payment_due,'%Y-%m-%d').strftime('%d-%b-%Y')

            newEntry = {
                "email":email,
                "name":name,
                "etsy_id":etsy_id,
                "period":period,
                "start_date":start_date_obj,
                "end_date":end_date_obj,
                "renewal_date":renewal_date_obj,
                "sold_price":sold_price,
                "new_price":new_price,
                "payment_due":payment_due_obj
            }             
            if category == "thirty_five_pound":           
                db.thirty_five_pound.insert_one(newEntry)
            elif category == "fourty_pound":           
                db.fourty_pound.insert_one(newEntry)
            elif category == "fourty_five_pound":           
                db.fourty_five_pound.insert_one(newEntry)
            elif category == "fifty_pound":           
                db.fifty_pound.insert_one(newEntry)
            elif category == "sixty_five_pound":           
                db.sixty_five_pound.insert_one(newEntry)
            elif category == "family_subscriptions":           
                db.family_subscriptions.insert_one(newEntry)
            return redirect(url_for(category))

        else:
            if category == "thirty_five_pound":
                data = ["35","thirty_five_pound"]
            elif category == "fourty_pound":
                data = ["40","fourty_pound"]
            elif category == "fourty_five_pound":
                data = ["45","fourty_five_pound"]
            elif category == "fifty_pound":
                data = ["50","fifty_pound"]
            elif category == "sixty_five_pound":
                data = ["65","sixty_five_pound"]
            elif category == "family_subscriptions":
                data = ["Family","family_subscriptions"]
            
            return render_template("add-subscription.html",data=data)

# delete subscription route 
@app.route("/delete-subscription/<string:category>/<id>")
def date(category,id):
    if 'loggedin' in session:
        query = {"_id":ObjectId(id)}             
        if category == "thirty_five_pound":           
            db.thirty_five_pound.delete_one(query)
        elif category == "fourty_pound":           
            db.fourty_pound.delete_one(query)
        elif category == "fourty_five_pound":           
            db.fourty_five_pound.delete_one(query)
        elif category == "fifty_pound":           
            db.fifty_pound.delete_one(query)
        elif category == "sixty_five_pound":           
            db.sixty_five_pound.delete_one(query)
        return redirect(url_for(category))
    else:
        return redirect(url_for("login"))

# edit subscription route 
@app.route("/edit-subscription/<string:category>/<id>",methods=['GET','POST'])
def edit_subscription(category,id):    
    if 'loggedin' in session:
        if request.method == 'POST':            
            email = request.form.get("email")
            name = request.form.get("name")
            etsy_id = request.form.get("etsy_id")
            period = request.form.get("period")
            sold_price = request.form.get("sold_price")
            new_price = request.form.get("new_price")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            renewal_date = request.form.get("renewal_date")
            payment_due = request.form.get("payment_due")


            newvalues = {
            "$set": {
                "email":email,
                "name":name,
                "etsy_id":etsy_id,
                "period":period,
                "start_date":start_date,
                "end_date":end_date,
                "renewal_date":renewal_date,
                "sold_price":sold_price,
                "new_price":new_price,
                "payment_due":payment_due
            }
            }
            filter = {'_id': ObjectId(id)}            
            if category == "thirty_five_pound":   
                db.thirty_five_pound.update_one(filter, newvalues)
            elif category == "fourty_pound":   
                db.fourty_pound.update_one(filter, newvalues)   
            elif category == "fourty_five_pound":   
                db.fourty_five_pound.update_one(filter, newvalues)   
            elif category == "fifty_pound":   
                db.fifty_five_pound.update_one(filter, newvalues)    
            elif category == "sixty_five_pound":   
                db.sixty_five_pound.update_one(filter, newvalues)    
            elif category == "family_subscriptions":   
                db.family_subscriptions.update_one(filter, newvalues)    
            return redirect(url_for(category))
            
        else:
            query = {"_id":ObjectId(id)}
            if category == "thirty_five_pound":                
                subscription = db.thirty_five_pound.find_one(query)
                data = ["35","thirty_five_pound"]
            elif category == "fourty_pound":                
                subscription = db.fourty_pound.find_one(query)
                data = ["40","fourty_pound"]
            elif category == "fourty_five_pound":                
                subscription = db.fourty_five_pound.find_one(query)
                data = ["45","fourty_five_pound"]
            elif category == "fifty_pound":                
                subscription = db.fifty_pound.find_one(query)
                data = ["50","fifty_pound"]
            elif category == "sixty_five_pound":                
                subscription = db.sixty_five_pound.find_one(query)
                data = ["65","sixty_five_pound"]
            elif category == "family_subscriptions":                
                subscription = db.family_subscriptions.find_one(query)
                data = ["Family","family_subscriptions"]
            return render_template("edit-subscription.html",data=data,sub=subscription)
    else:
        return redirect(url_for("login"))

# admin account route 
@app.route("/admin-account")
def admin_account():
    if 'loggedin' in session:
        adminData = db.admin.find_one()
        return render_template("account.html",data=adminData)
    else:
        return redirect(url_for('login'))
# edit admin account route 
@app.route("/edit-admin-account", methods=['GET','POST'])
def edit_admin_account():
    if 'loggedin' in session:
        if request.method == 'POST':            
            adminData = db.admin.find_one()
            username = request.form.get("username")
            password = request.form.get("password")
            c_password = request.form.get("c_password")
            print(username)
            print(password)
            print(c_password)
            if not username or not password or not c_password:
                return render_template("edit-account.html",data=adminData, msg="Missing Data")                
            else:
                if password == c_password:
                    newvalues = {
                    "$set": {
                        "username":username,
                        "password":password,
                    }
                    }
                    filter = {'_id': ObjectId(adminData['_id'])}   
                    db.admin.update_one(filter, newvalues)
                    return redirect(url_for("admin_account"))                    
                else:
                    return render_template("edit-account.html",data=adminData, msg="Passwords doesn't match")     

        else:
            adminData = db.admin.find_one()
            return render_template("edit-account.html",data=adminData)
    else:
        return redirect(url_for('login'))

# all subscriptions route 
@app.route("/all-subscriptions")
def all_subscriptions():
    if 'loggedin' in session:        
        data1 = db.thirty_five_pound.find()
        data2 = db.fourty_pound.find()
        data3 = db.fourty_five_pound.find()
        data4 = db.fifty_pound.find()
        data5 = db.sixty_five_pound.find()
        data6 = db.family_subscriptions.find()
        lists = []
        for i in data1:            
            i.update({"_id": str(i["_id"]),"category":"35"})
            lists.append(i)
        for i in data2:            
            i.update({"_id": str(i["_id"]),"category":"40"})
            lists.append(i)
        for i in data3:            
            i.update({"_id": str(i["_id"]),"category":"45"})
            lists.append(i)
        for i in data4:            
            i.update({"_id": str(i["_id"]),"category":"50"})
            lists.append(i)
        for i in data5:            
            i.update({"_id": str(i["_id"]),"category":"65"})
            lists.append(i)
        for i in data6:            
            i.update({"_id": str(i["_id"]),"category":"Family"})
            lists.append(i)
        return render_template("all-subscriptions.html",data=lists)
    else:
        return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)