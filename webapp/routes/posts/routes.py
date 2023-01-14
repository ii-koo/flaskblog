# this route used for post page
from flask import render_template, url_for, redirect, flash, request, abort, Blueprint
from webapp.routes.posts.forms import PostForm, UpdateAccountForm
from flask_login import login_required, current_user
from webapp.routes.utils import save_picture
from webapp.models.model import Post, User
from webapp import db

posts = Blueprint('posts', '__name__')


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(viewed=1, title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post "{form.title.data}" has been created!', "success")
        return redirect(url_for('main.index'))
    return render_template('pages/posts/newPost.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>')
def postDetail(post_id):
    latest_posts = Post.query.order_by(Post.date_created.desc())
    popular_posts = Post.query.order_by(Post.viewed.desc())

    post = Post.query.get_or_404(post_id)
    post.viewed = post.viewed + 1
    db.session.commit()
    return render_template('pages/posts/postDetail.html', title=post.title, post=post, latest_posts=latest_posts, popular_posts=popular_posts)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def postUpdate(post_id):
    latest_posts = Post.query.order_by(Post.date_created.desc())
    popular_posts = Post.query.order_by(Post.viewed.desc())

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post "{form.title.data}" has been updated!', "success")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('pages/posts/postUpdate.html', title='Update '+post.title, form=form, latest_posts=latest_posts, popular_posts=popular_posts)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post "{post.title}" has been deleted!', "success")
    return redirect(url_for('main.index'))


@posts.route('/user/<string:username>')
def userPosts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).\
        order_by(Post.date_created.desc()).\
        paginate(page=page, per_page=5)
    return render_template('pages/posts/userPosts.html', title='Home', posts=posts, user=user)


@posts.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile/' + current_user.image_file)
    return render_template('pages/account/account.html', title='Account', image_file=image_file, form=form)