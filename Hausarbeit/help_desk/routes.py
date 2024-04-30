from help_desk import app, db, s
from flask import flash, redirect, render_template, request, url_for, make_response
from sqlalchemy import text
import re

@app.route('/')
def homepage():
    cookie = request.cookies.get('name')
    return render_template("home.html", cookie=cookie)

@app.route('/user_story_details')
def user_story_details():
    cookie = request.cookies.get('name')
    if not cookie:
        return redirect(url_for('login'))
    query = text("SELECT * FROM user_story")
    print(query)
    result = db.session.execute(query)
    user_stories = result.fetchall()
    return render_template("user_story_details2.html", user_stories=user_stories, cookie=cookie)

@app.route('/user_story_create', methods=['GET', 'POST'])
def user_story_create():
    cookie = request.cookies.get('name')
    if not cookie:
        return redirect(url_for('login'))
    if request.method == "POST":
        title = request.form['title']
        story_points = request.form['story_points']
        story_points = int(story_points)
        status = request.form['status']        
        created_by = request.form['created_by']
        print(f"Title: {title} with story points {story_points}")
        print(f"Status: {status}")
        print(f"Created by: {created_by}")
        if title is None or isinstance(title, str) is False or len(title) < 10:
            print("Not valid - Title")
            flash(f"Title is not valid", category="danger")
            return render_template("user_story_create.html")
        if story_points is None or isinstance(story_points, int) is False or story_points < 1:
            print("Not valid - Story Points")
            flash(f"Story Points are not valid", category="danger")
            return render_template("user_story_create.html")
        if status is None or isinstance(status, str) is False or len(status) < 3:
            print("Not valid - Status")
            flash(f"Status is not valid", category="danger")
            return render_template("user_story_create.html")
        if created_by is None or isinstance(created_by, str) is False or len(created_by) < 3:
            print("Not valid - Created By")
            flash(f"Created By is not valid", category="danger")
            return render_template("user_story_create.html")
        query = text(f"INSERT INTO user_story (title, story_points, status, created_by) VALUES ('{title}', {story_points}, '{status}', '{created_by}')")
        print(query)
        db.session.execute(query)
        db.session.commit()
        flash(f"User Story: {title} was successfully created", category="success")
        return redirect(url_for('user_story_details'))
        
    return render_template("user_story_create.html", cookie=cookie)

@app.route('/user_story_edit/<int:id>', methods=['GET', 'POST'])
def user_story_edit(id):
    if request.method == 'POST':
        title = request.form['title']
        story_points = request.form['story_points']
        story_points = int(story_points)
        status = request.form['status']        
        created_by = request.form['created_by']
        print(f"Title: {title} with story points {story_points}")
        print(f"Status: {status}")
        print(f"Created by: {created_by}")
        if title is None or isinstance(title, str) is False or len(title) < 10:
            print("Not valid - Title")
            flash(f"Title is not valid", category="danger")
            return render_template("user_story_update.html")
        if story_points is None or isinstance(story_points, int) is False or story_points < 1:
            print("Not valid - Story Points")
            flash(f"Story Points are not valid", category="danger")
            return render_template("user_story_update.html")
        if status is None or isinstance(status, str) is False or len(status) < 3:
            print("Not valid - Status")
            flash(f"Status is not valid", category="danger")
            return render_template("user_story_update.html")
        if created_by is None or isinstance(created_by, str) is False or len(created_by) < 3:
            print("Not valid - Created By")
            flash(f"Created By is not valid", category="danger")
            return render_template("user_story_update.html")        
        query = text(f"UPDATE user_story SET title = '{title}', story_points = {story_points}, status = '{status}', created_by = '{created_by}' WHERE id = {id}")
        print(query)        
        db.session.execute(query)
        db.session.commit()
        flash(f"User Story: {title} was successfully updated", category="success")
        return redirect(url_for('user_story_details'))
    return render_template("user_story_update.html", id=id)

@app.route('/user_story_delete/<int:id>', methods=['GET', 'POST'])
def user_story_delete(id):
    if request.method == 'POST':
        query_select = text(f"SELECT title FROM user_story WHERE id = {id}")
        result = db.session.execute(query_select)
        user_story = result.fetchall()
        query_delete = text(f"DELETE FROM user_story WHERE id = {id}")
        db.session.execute(query_delete)
        db.session.commit()
        flash(f"The user story with the title {user_story[0]} was succesfully deleted", category="success")
        return redirect(url_for('user_story_details'))
    return render_template("user_story_delete.html", id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"User: {username} with password {password}")
        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("Not valid - Username")
            flash(f"Username is not valid", category="danger")
            return render_template("login.html", error="Invalid username")
        if password is None or isinstance(password, str) is False or len(password) < 3:
            print("Not valid - Password")
            flash(f"Password is not valid", category="danger")
            return render_template("login.html", error="Invalid password")
        query = f"select username from users where username = '{username}' and passwd = '{password}'"
        print(query)
        result = db.session.execute(text(query))        
        #query = "SELECT username FROM users WHERE username = :username AND passwd = :password"
        #result = db.session.execute(text(query), {"username": username, "password": password})
        user = result.fetchall()
        print(user)
        if user:
            flash(f"{user} you are logged in", category="success")
            #resp = render_template("home.html", cookie=username)
            encrypted_cookie = s.dumps({'username': username})
            resp = make_response(redirect(url_for('homepage')))
            resp.set_cookie('name', encrypted_cookie)
            return resp
            
        print("Invalid credentials")
        flash(f"The user with the name: {user} does not exist", category="danger")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_confirm = request.form['password_confirm']
        print(f"User: {username} with password {password}")
        print(f"Email: {email}")
        print(f"Password Confirm: {password_confirm}")
        if username is None or isinstance(username, str) is False or len(username) < 3:
            print("Not valid - Username")
            flash(f"Username is not valid", category="danger")
            return render_template("register.html")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            print("Not valid - Email")
            flash(f"Email is not valid", category="danger")
            return render_template("register.html")
        if password is None or isinstance(password, str) is False or len(password) < 3:
            print("Not valid - Password")
            flash(f"Password is not valid", category="danger")
            return render_template("register.html")
        if password != password_confirm:
            print("Not valid - Password does not match")
            flash(f"Passwords do not match", category="danger")
            return render_template("register.html")
        
        query_select = text(f"SELECT username FROM users WHERE username = '{username}'")
        result = db.session.execute(query_select)
        user = result.fetchall()
        print(user)
        if user:
            flash(f"User with the name: {user} already exists", category="danger")
            return render_template("register.html")
        query_insert = text(f"INSERT INTO users (username, email, passwd) VALUES ('{username}', '{email}', '{password}')")
        db.session.execute(query_insert)
        db.session.commit()
        flash(f"User {username} was successfully registered", category="success")
        encrypted_cookie = s.dumps({'username': username})
        resp = make_response(redirect(url_for('homepage')))
        resp.set_cookie('name', encrypted_cookie)
        return resp
    return render_template("register.html")

@app.route('/logout')
def logout():
    print("->logout()")
    resp = redirect('/login')
    resp.set_cookie('name', '', expires=0)
    print("<-logout()")
    return resp