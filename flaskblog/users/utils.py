
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('密码重置请求',
                  sender='wsj@centuryw.cn',
                  recipients=[user.email])
    msg.body = f'''重置密码请访问下面的链接:
{url_for('users.reset_token', token=token, _external=True)}

如果你没有做此操作，请忽略此邮件
'''
    mail.send(msg)
