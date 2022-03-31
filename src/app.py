from flask import Flask, redirect, request, render_template, flash, session, url_for

import post
import user
from config import Config
from helper_funcs import *

app = Flask(__name__)
app.secret_key = "Rand:)"


@app.route('/')
def index():
    return render_template('index.html')


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the input data
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if missing
        if not username or not password:
            flash('Username and password are required ...', 'error')
            return render_template('login.html')
        else:
            response = userInstance.login(username, password)
            # login failed
            if response.has_errors():
                for err in response.errors:
                    flash(err, 'error')
                return render_template('login.html')
            # login success
            else:
                userInstance.start_session(response.data['username'])
                return redirect(url_for('posts'))

    elif request.method == 'GET':
        if session.get('username'):
            flash('You are logged in!', 'success')
            return redirect(url_for('index'))

        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the input data
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if missing
        if not name or not username or not password:
            flash('Name,username and password are required ...', 'error')
            return redirect(url_for('signup'))
        else:
            response = userInstance.signup(name, username, password)
            if response.has_errors():
                for err in response.errors:
                    flash(err, 'error')
                return redirect(url_for('signup'))
            # registration success
            else:
                userInstance.start_session(response.data['username'])
                flash('Registered successfully!', 'success')
                return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('signup.html')


@app.route('/logout')
def logout():
    if session.get('username'):
        if userInstance.logout():
            flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    response = postInstance.get_all()
    if response.has_errors():
        flash('No posts yet ...', 'error')
    return render_template('posts.html', posts=response.data)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required()
def add_post():
    if request.method == 'POST':
        # Get the input data
        title = request.form.get('title')
        description = request.form.get('description')
        # Check if missing
        if not title or not description:
            flash('title and description are required ...', 'error')
            return redirect(url_for('add_post'))
        else:
            response = postInstance.add(title, description,
                                        userInstance.get_user_id(session.get('username')).data['id'])
            flash('Post added successfully...', 'success')
            return redirect(url_for('posts'))
    else:
        return render_template('add_post.html')


@app.route('/delete_post', methods=['POST'])
@login_required()
def delete_post():
    id = request.form.get('id')
    if postInstance.delete(id):
        flash('Post deleted ...', 'success')
    else:
        flash('Delete failed! ...', 'error')
    return redirect(url_for('posts'))


userInstance = user.User(Config)
postInstance = post.Post(Config)

if __name__ == '__main__':
    app.run()
