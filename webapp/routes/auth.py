from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from webapp.forms.form import RegisterForm, LoginForm
from webapp.models.model import User
from webapp import app, bcrypt, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else redirect(url_for('index')))
        else:
            flash(f"Login unsuccessful, Please check username and password", 'danger')
            return redirect(url_for('login'))
    return render_template('auth/login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('index'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))