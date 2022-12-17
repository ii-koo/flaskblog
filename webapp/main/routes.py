# This file used for main page route
from flask import request, render_template, Blueprint
from webapp.models.model import Post

main = Blueprint('main', '__name__')


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_created.desc()).paginate(page=page, per_page=5)
    return render_template('pages/index.html', title='Home', posts=posts)


@main.route('/about')
def about():
    return render_template('pages/about.html', title='About')
