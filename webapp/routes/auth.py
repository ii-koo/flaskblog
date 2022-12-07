from flask import render_template, redirect, url_for, flash
from webapp.forms.form import RegisterForm, LoginForm
from webapp import app


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('auth/login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", 'success')
        return redirect(url_for('index'))
    return render_template('auth/register.html', title='Register', form=form)