from flask import Flask, render_template

app = Flask(__name__)


posts = [
    {
        'title': 'First Post',
        'author': 'Moderator',
        'content': 'i made a first post',
        'date_posted': 'April 03, 2021'
    }, {
        'title': 'Second Post',
        'author': 'User',
        'content': 'i made a first post',
        'date_posted': 'April 04, 2021'
    }
]


@app.route('/')
def index():
    return render_template('pages/index.html', title='Home', posts=posts)


@app.route('/about')
def about():
    return render_template('pages/about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True, port=3000)