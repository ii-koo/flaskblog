# This file used for main page route
from flask import request, render_template, Blueprint
from webapp.models.model import Post

main = Blueprint('main', '__name__')


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    latest_posts = Post.query.order_by(Post.date_created.desc())
    popular_posts = Post.query.order_by(Post.viewed.desc())
    return render_template('pages/index.html', title='Home', posts=posts, latest_posts=latest_posts, popular_posts=popular_posts)


@main.route('/about')
def about():
    latest_posts = Post.query.order_by(Post.date_created.desc())
    popular_posts = Post.query.order_by(Post.viewed.desc())
    return render_template('pages/about.html', title='About', latest_posts=latest_posts, popular_posts=popular_posts)
