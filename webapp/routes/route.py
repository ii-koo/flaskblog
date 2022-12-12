from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from webapp.forms.form import UpdateAccountForm, PostForm
from webapp.models.model import Post
from webapp import app, db
from PIL import Image
import secrets
import os

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
    posts = Post.query.all()
    return render_template('pages/index.html', title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template('pages/about.html', title='About')


@login_required
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile/' + current_user.image_file)
    return render_template('pages/account/account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(viewed=1, title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post "{form.title.data}" has been created!', "success")
        return redirect(url_for('index'))
    return render_template('pages/posts/newPost.html', title='New Post', form=form)