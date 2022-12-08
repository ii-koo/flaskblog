from flask import render_template
from flask_login import login_required
from webapp import app

posts = [
    {
        'title': 'First Post',
        'author': 'Moderator',
        'content': 'i made a first post',
        'date_posted': 'April 03, 2021'
    }, {
        'title': 'Second Post',
        'author': 'User',
        'content': 'i made a second post',
        'date_posted': 'April 04, 2021'
    }
]


@app.route('/')
def index():
    return render_template('pages/index.html', title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template('pages/about.html', title='About')


@app.route('/account')
@login_required
def account():
    return render_template('pages/account/account.html', title='Account')