from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt   
from datetime import datetime 
import re
SCHEMA = "trainrdb"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
INVALID_PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "tacocat"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register_user():
    is_valid = True
    
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("First name must be at least 2 characters long")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters long")
    if len(request.form['password']) < 8:
        is_valid = False
        flash("Password must be at least 8 characters long")
    if request.form['c_password'] != request.form['password']:
        is_valid = False
        flash("Passwords must match")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Please use a valid email address")
    else:
        mysql= connectToMySQL(SCHEMA)
        query = "SELECT * FROM user WHERE email = %(email)s"
        data ={
            'email': request.form['email']
        }
        user = mysql.query_db(query,data)
        if user:
            is_valid = False
            flash("Email already in use")

    if is_valid:
        mysql = connectToMySQL(SCHEMA)
        # build my query
        query = "INSERT INTO user (first_name, last_name, password, email, created_at, updated_at,adminlevel) VALUES (%(fn)s, %(ln)s, %(pass)s, %(email)s, NOW(), NOW(), 0)"
        # pass revlevant to with my query
        data = {
            'fn': request.form['first_name'],
            'ln': request.form['last_name'],
            'pass': bcrypt.generate_password_hash(request.form['password']),
            'email': request.form['email']
        }
        # commit the query
        user_id = mysql.query_db(query, data)
        session['user_id'] = user_id
        session['name'] = request.form['first_name']
        session['email'] = request.form['email']
        return redirect("/dashboard")
    else: # otherwise, reidrect and show errors
        return redirect("/")

@app.route("/login", methods=["POST"])
def login_user():
    if len(request.form['email']) < 1 or len (request.form['password']) <1:
        flash("Email and passsword is required")
    else:
        mysql = connectToMySQL(SCHEMA)
        query = "SELECT * FROM user WHERE user.email = %(email)s"
        data = {
            'email': request.form['email']
        }
        user = mysql.query_db(query, data)
        if user:
            if bcrypt.check_password_hash(user[0]['password'], request.form['password']):
                session['user_id'] = user[0]['id']
                session['name'] = user[0]['first_name']
                session['email'] = user[0]['email']
                return redirect("/dashboard")
        else:
            flash("Email and password do not match")
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_workout WHERE user_id = %(session)s"
    data = {
        'session': session['user_id']
    }
    my_workout = mysql.query_db(query,data)
    return render_template("dashboard.html", my_workout = my_workout)

@app.route("/addworkout", methods=['POST'])
def add_workout():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    
    if len(request.form['name']) < 3:
        is_valid = False
        flash("Workout must be at least 3 characters long")
    if is_valid:
        mysql = connectToMySQL(SCHEMA)
        query = "INSERT INTO user_workout(name, set_num, rep, created_at, updated_at, user_id) VALUES (%(item)s,%(num)s,%(rep)s, NOW(),NOW(), %(id)s)"
        data = {
            'item': request.form['name'], 
            'num': request.form['num'],
            'rep': request.form['rep'],
            'id': session['user_id']
        }
        this_workout = mysql.query_db(query, data)
        return redirect("/dashboard")
    else:
        return redirect("/workout/new")

@app.route("/workout/new")
def new_workout():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("newworkout.html")

@app.route("/addsuggestion", methods=['POST'])
def add_suggestion():
    if 'user_id' not in session:
        return redirect("/")
    is_valid = True
    
    if len(request.form['text']) < 3:
        is_valid = False
        flash("suggestion must be at least 3 characters long")
    if is_valid:
        mysql = connectToMySQL(SCHEMA)
        query = "INSERT INTO user_suggestions(suggestion, created_at, updated_at, user_id) VALUES (%(item)s, NOW(),NOW(), %(id)s)"
        data = {
            'item': request.form['text'],
            'id': session['user_id']
        }
        this_suggestion = mysql.query_db(query, data)
        return redirect("/communications")
    else:
        return redirect("/dashboard")

@app.route("/communications")
def view_suggestion():
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_suggestions WHERE user_id = %(session)s"
    data = {
        'session': session['user_id']
    }
    user_suggestion = mysql.query_db(query,data)    
    return render_template("comm.html", user_suggestion = user_suggestion)

@app.route("/admin/dashboard")
def view_users():
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user"
    all_user = mysql.query_db(query)
    return render_template("admindash.html", all_user = all_user)    
  
@app.route("/admin/communications/<u_id>")
def view_comms(u_id):
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user WHERE id = %(id)s"
    data = {
        'id': int(u_id)
    }
    user_info = mysql.query_db(query,data)    
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_suggestions"
    user_suggestion = mysql.query_db(query)    
    return render_template("client.html", user_suggestion = user_suggestion, user_info = user_info[0])


@app.route("/user/<u_id>")
def user(u_id):
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user WHERE id = %(id)s"
    data = {
        'id': int(u_id)
    }
    user_info = mysql.query_db(query, data)
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_suggestions"
    user_suggestion = mysql.query_db(query)
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_workout"
    user_workout = mysql.query_db(query)
    return render_template("client.html", user_suggestion = user_suggestion, user_info = user_info[0], user_workout = user_workout)

@app.route("/workout/remove/<item_id>")
def remove_item(item_id):
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_workout WHERE id = %(i_id)s AND user_id = %(session)s"
    data = {
        'session': session['user_id'],
        'i_id': int(item_id)
    }
    this_item= mysql.query_db(query,data)
    if this_item:
        mysql = connectToMySQL(SCHEMA)
        query = "DELETE FROM user_workout WHERE id = %(i_id)s AND user_id = %(session)s"
        data = {
            'session': session['user_id'],
            'i_id': int(item_id)
        }
        this_item= mysql.query_db(query,data)
    return redirect("/dashboard")

@app.route("/suggestion/remove/<item_id>")
def remove_suggestion(item_id):
    if 'user_id' not in session:
        return redirect("/")
    mysql = connectToMySQL(SCHEMA)
    query = "SELECT * FROM user_suggestions WHERE id = %(i_id)s AND user_id = %(session)s"
    data = {
        'session': session['user_id'],
        'i_id': int(item_id)
    }
    this_item= mysql.query_db(query,data)
    if this_item:
        mysql = connectToMySQL(SCHEMA)
        query = "DELETE FROM user_suggestions WHERE id = %(i_id)s AND user_id = %(session)s"
        data = {
            'session': session['user_id'],
            'i_id': int(item_id)
        }
        this_item= mysql.query_db(query,data)
    return redirect("/communications")  

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)