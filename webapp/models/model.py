from webapp import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='default.png')
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=300):
        s = Serializer(current_app.config(['SECRET_KEY']), expires_sec)
        return s.dumps({'user.id': self.id}).decode('utf-8')

    """
    ketika metode ini dipanggil, kita tidak meneruskan instance kelas ke metode tersebut 
    (seperti yang biasa kita lakukan dengan metode). Ini berarti kita dapat meletakkan 
    fungsi di dalam kelas tetapi tidak dapat mengakses instance dari kelas tersebut 
    (ini berguna saat metode Anda tidak menggunakan instance).
    """
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewed = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)