import re
from flask import Flask, render_template, jsonify, request, session, url_for, redirect
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
import os
from flask_mail import Mail, Message
import json
from time import time
from flask_apscheduler import APScheduler

# set Flask scheduler configuration values
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)

# flask scheduler
app.config.from_object(Config())
# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)




    



# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_url)
client.list_database_names()
database_name = "subscriptions"
db = client[database_name]

# configure secret key for session
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.ionos.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'fakhar@web-designpakistan.com'
app.config['MAIL_PASSWORD'] = 'alikhaliqwebdesign!@#'
app.config['MAIL_DEFAULT_SENDER'] = ('fakhar@web-designpakistan.com', "fakhar@web-designpakistan.com")
mail = Mail(app)


# interval example
@scheduler.task('interval', id='do_job_1', seconds=60, misfire_grace_time=9)
def job1():
    print('Job 1 executed')
    return sendmail()

def sendmail():
    try:
        with app.app_context():
            query = {"status":"pending"}
            data = db.schedule_emails.find(query)
            for i in data:
                payment_due = i['payment_due']
                payment_due = payment_due.date()
                print(payment_due)
                today = datetime.now()
                today = today.date()
                print(today)
                # minutes_diff = (payment_due - today).total_seconds() / 60.0
                # minutes_diff = round(minutes_diff)
                # print(minutes_diff)
                if today == payment_due:
                    msg = Message("Your subscription is about to end!",sender='fakhar@web-designpakistan.com', recipients=[i['email']])
                    msg.html = str("Dear, "+i['email']+"! Your Subscription is about to end soon please renew your subscription asap.")
                    mail.send(msg)
                    print("email sent")
                    newvalues = {
                    "$set": {
                        'status': "completed"
                    }
                    }
                    filter = {'_id': ObjectId(i['_id'])}
                    db.schedule_emails.update_one(filter, newvalues)
                    print("database updated")
    except Exception as e:
        return str(e)

@app.route("/error")
def error():
    return render_template("error.html")
@app.route("/")
def index():
    if 'loggedin' in session:
        one = db.thirty_five_pound.count()
        two = db.fourty_pound.count()
        three = db.fourty_five_pound.count()
        four = db.fifty_pound.count()
        five = db.sixty_five_pound.count()
        six = db.family_subscriptions.count()
        seven = db.zam_subscriptions.count()
        data = [one,two,three,four,five,six,seven]
        return render_template("index.html",data=data)
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

# zam subsctiptions route
@app.route("/zam_subscriptions")
def zam_subscriptions():
    if 'loggedin' in session:
        data = db.zam_subscriptions.find()
        lists = []
        for i in data:            
            i.update({"_id": str(i["_id"])})
            lists.append(i)
        print(lists)
        return render_template("zam_subscriptions.html",data=lists)
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
            if not email or not name or not etsy_id or not period or not sold_price or not new_price or not start_date or not end_date or not renewal_date or not payment_due:
                return render_template("error.html",error = "Missing Data!")
            payment_due2 = str(payment_due)+" 00:00:00.000000"
            date_time = datetime.strptime(payment_due2, '%Y-%m-%d %H:%M:%S.%f')

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
            elif category == "zam_subscriptions":           
                db.zam_subscriptions.insert_one(newEntry)
            # store schedule email data into mongodatabase 
            new_schedule = {
                "email": email,
                "payment_due":date_time,
                "status":"pending"
            }
            db.schedule_emails.insert_one(new_schedule)
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
            elif category == "zam_subscriptions":
                data = ["Zam","zam_subscriptions"]
            
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
        elif category == "family_subscriptions":           
            db.family_subscriptions.delete_one(query)
        elif category == "zam_subscriptions":           
            db.zam_subscriptions.delete_one(query)
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
            elif category == "zam_subscriptions":   
                db.zam_subscriptions.update_one(filter, newvalues)    
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
            elif category == "zam_subscriptions":                
                subscription = db.zam_subscriptions.find_one(query)
                data = ["Zam","zam_subscriptions"]
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
        data7 = db.zam_subscriptions.find()
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
        for i in data7:            
            i.update({"_id": str(i["_id"]),"category":"Zam"})
            lists.append(i)
        return render_template("all-subscriptions.html",data=lists)
    else:
        return redirect(url_for("login"))

@app.route("/report")
def report():  
    if "loggedin" in session:
        a = db.thirty_five_pound.find()
        b = db.fourty_pound.find()
        c = db.fourty_five_pound.find()
        d = db.fifty_pound.find()
        e = db.sixty_five_pound.find()
        f = db.family_subscriptions.find()
        g = db.zam_subscriptions.find()
        lists = []
        prices = []
        for i in a:            
            i.update({"_id": str(i["_id"]),"category":"35"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in b:            
            i.update({"_id": str(i["_id"]),"category":"40"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in c:            
            i.update({"_id": str(i["_id"]),"category":"45"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in d:            
            i.update({"_id": str(i["_id"]),"category":"50"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in e:            
            i.update({"_id": str(i["_id"]),"category":"65"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in f:            
            i.update({"_id": str(i["_id"]),"category":"Family"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        for i in g:            
            i.update({"_id": str(i["_id"]),"category":"Zam"})
            sold_price = float(i["sold_price"])
            prices.append(sold_price)
            lists.append(i)
        total = sum(map(float,prices))
        total_subs = len(lists)

        
        one = db.thirty_five_pound.count()
        two = db.fourty_pound.count()
        three = db.fourty_five_pound.count()
        four = db.fifty_pound.count()
        five = db.sixty_five_pound.count()
        six = db.family_subscriptions.count()
        seven = db.zam_subscriptions.count()
        data = [one,two,three,four,five,six,seven]
        return render_template("report.html",total_price = total, total_subs = total_subs, data=data)
    else:
        return redirect(url_for("login"))


scheduler.start()
if __name__ == '__main__':
    app.run(debug=True)