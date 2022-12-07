from flask import render_template, redirect
from webapp.forms.form import RegisterForm, LoginForm
from webapp import app


@app.route('/login')
def login():
    return render_template('auth/login.html', title='Login')


@app.route('/register')
def register():
    return render_template('auth/register.html', title='Register')