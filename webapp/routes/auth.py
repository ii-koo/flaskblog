from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from webapp.forms.form import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from webapp.models.model import User
from webapp import app, bcrypt, db, mail


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
            return redirect(next_page) if next_page else redirect(url_for('index'))
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


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset', sender='noreply@demo.com', recipients=[user])
    message.body = f"""
    To reset your password, please visit the following link:
    {url_for('reset_password', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will be made.
    """


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_req():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instrunctions to reset your password", 'info')
        return redirect(url_for('login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_req'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated", 'success')
        return redirect(url_for('index'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)