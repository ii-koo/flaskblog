import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_login import login_required


@login_required
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/profile', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset', sender='noreply@demo.com', recipients=[user])
    message.body = f"""
    To reset your password, please visit the following link:
    {url_for('reset_password', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will be made.
    """