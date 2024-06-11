from functools import wraps
import subprocess
from help_desk import app, db, limiter
from flask import flash, redirect, render_template, request, url_for, session
from flask_wtf import Form
from markupsafe import Markup
from sqlalchemy import text
from help_desk.form_validation import RegistrationForm, UserStoryForm, UserStoryDeleteForm, LoginForm

"""
def verify_user(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'name' in request.cookies:
            encrypted_cookie = request.cookies.get('name')
            try:
                username = s.loads(encrypted_cookie)['username']
                query = text(f"SELECT username FROM users WHERE username = '{username}'")
                result = db.session.execute(query)
                user = result.fetchone()
                if user:
                    return func(*args, **kwargs)
            except Exception as e:
                print(e)
                flash("Invalid user cookie.", category="danger")
                return redirect(url_for('login'))
        flash("User cookie not found.", category="danger")
        return redirect(url_for('login'))
    return decorated_function
"""

@app.route('/')
def homepage():
    if 'username' in session:
        return render_template("home.html", cookie=session['username'])
    """
    if cookie:
        try:
            username = s.loads(cookie)['username']
            query = text(f"SELECT username FROM users WHERE username = '{username}'")
            result = db.session.execute(query)
            user = result.fetchone()
            if user:
                return render_template("home.html", cookie=username)
        except Exception as e:
            query = text(f"SELECT username FROM users WHERE username = '{cookie}'")
            result = db.session.execute(query)
            user = result.fetchone()
            if user:
                encrypted_cookie = s.dumps({'username': cookie})
                resp = make_response(render_template("home.html", cookie=cookie))
                resp.set_cookie('name', encrypted_cookie)
                return resp
            else:
                resp = make_response(redirect(url_for('login')))
                resp.set_cookie('name', '', expires=0)
                flash("Invalid user cookie.", category="danger")
                return resp
    """
    return render_template("home.html")

@app.route('/user_story_details')
def user_story_details():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = text("SELECT * FROM user_story")    
    print(query)
    result = db.session.execute(query)
    user_stories = result.fetchall()
    return render_template("user_story_details2.html", user_stories=user_stories, cookie=session['username'])

@app.route('/user_story_create', methods=['GET', 'POST'])
def user_story_create():
    if 'username' not in session:
        return redirect(url_for('login'))
    #form = UserStoryForm(request.form)
    if request.method == "POST":
        title = request.form['title']
        story_points = request.form['story_points']
        story_points = int(story_points)
        status = request.form['status']
        created_by = request.form['created_by']
        """
        title = form.title.data
        story_points = form.story_points.data
        status = form.status.data
        created_by = form.created_by.data
        
        title = Markup.escape(request.form['title'])
        story_points = Markup.escape(request.form['story_points'])
        story_points = int(story_points)
        status = Markup.escape(request.form['status'])        
        created_by = Markup.escape(request.form['created_by'])
        """
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
        #query = "INSERT INTO user_story (title, story_points, status, created_by) VALUES (:title, :story_points, :status, :created_by)"
        #db.session.execute(text(query), {"title": title, "story_points": story_points, "status": status, "created_by": created_by})
        print(query)
        db.session.execute(query)
        db.session.commit()
        flash(f"User Story: {title} was successfully created", category="success")
        return redirect(url_for('user_story_details'))
        
    return render_template("user_story_create.html", cookie=session['username'])

@app.route('/user_story_edit/<int:id>', methods=['GET', 'POST'])
def user_story_edit(id):
    #form = UserStoryForm(request.form)
    if request.method == 'POST':
        title = request.form['title']
        story_points = request.form['story_points']
        story_points = int(story_points)
        status = request.form['status']        
        created_by = request.form['created_by']
        """
        title = form.title.data
        story_points = form.story_points.data
        status = form.status.data
        created_by = form.created_by.data

        escape die Daten noch später
        """
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
        #query = "UPDATE user_story SET title = :title, story_points = :story_points, status = :status, created_by = :created_by WHERE id = :id"
        #db.session.execute(text(query), {"title": title, "story_points": story_points, "status": status, "created_by": created_by, "id": id})
        print(query)        
        db.session.execute(query)
        db.session.commit()
        flash(f"User Story: {title} was successfully updated", category="success")
        return redirect(url_for('user_story_details'))
    return render_template("user_story_update.html", id=id)

@app.route('/user_story_delete/<int:id>', methods=['GET', 'POST'])
def user_story_delete(id):
    """
    form = UserStoryDeleteForm(request.form)
    if form.validate_on_submit():
    """
    if request.method == 'POST':
        
        if id == 0:
            query_delete = text("DELETE FROM user_story")
            db.session.execute(query_delete)
            db.session.commit()
            flash(f"All user stories were succesfully deleted", category="success")
            return redirect(url_for('user_story_details'))
        query_select = text(f"SELECT title FROM user_story WHERE id = {id}")
        #query = "SELECT title FROM user_story WHERE id = :id"
        #result = db.session.execute(text(query), {"id": id})
        result = db.session.execute(query_select)
        user_story = result.fetchall()
        query_delete = text(f"DELETE FROM user_story WHERE id = {id}")
        #query = "DELETE FROM user_story WHERE id = :id"
        #db.session.execute(text(query), {"id": id})
        db.session.execute(query_delete)
        db.session.commit()
        flash(f"The user story with the title {user_story[0]} was succesfully deleted", category="success")
        return redirect(url_for('user_story_details'))
    return render_template("user_story_delete.html", id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        """
        username = form.username.data
        password = form.password.data

        escape die Daten noch später
        """
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
            """
            #resp = render_template("home.html", cookie=username)
            print("User found")
            #username_split_2 = username[int(len(username)/2):]
            encrypted_cookie = s.dumps({'username': username})            
            resp = make_response(redirect(url_for('homepage')))
            resp.set_cookie('name', encrypted_cookie)
            return resp
            """
            session['username'] = username
            return redirect(url_for('homepage'))
            
        print("Invalid credentials")
        flash(f"The user does not exist", category="danger")

        return render_template("login.html", error="Invalid credentials", invalid_login=True)
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        password_confirm = form.confirm.data
        print(f"User: {username} with password {password}")
        print(f"Email: {email}")
        print(f"Password Confirm: {password_confirm}")

        """
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
        """
        
        query_select = text(f"SELECT username FROM users WHERE username = '{username}'")
        #query = "SELECT username FROM users WHERE username = :username"
        #result = db.session.execute(text(query), {"username": username})
        result = db.session.execute(query_select)
        user = result.fetchall()
        print(user)
        if user:
            flash(f"User with the name: {user} already exists", category="danger")
            return render_template("register.html")
        query_insert = text(f"INSERT INTO users (username, email, passwd) VALUES ('{username}', '{email}', '{password}')")
        #query = "INSERT INTO users (username, email, passwd) VALUES (:username, :email, :password)"
        #db.session.execute(text(query), {"username": username, "email": email, "password": password})
        db.session.execute(query_insert)
        db.session.commit()
        flash(f"User {username} was successfully registered", category="success")
        """
        encrypted_cookie = s.dumps({'username': username})
        
        resp = make_response(redirect(url_for('homepage')))
        resp.set_cookie('name', encrypted_cookie)
        """
        session['username'] = username
        return redirect(url_for('homepage'))
    return render_template("register.html", form=form)

@app.route('/shell', methods=['GET', 'POST'])
def shell():
    
    if request.method == 'POST':
        command = request.form['command']
        print(f"Command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True)
        print(result)
        if result.returncode == 0:
            return render_template('shell.html', output=result.stdout.decode('utf-8'))
        else:
            return render_template('shell.html', error=result.stderr.decode('utf-8'))

    return render_template('shell.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))