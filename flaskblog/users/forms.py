from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请换一个')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被使用，请换一个')


class LoginForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class UpdateAccountForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    picture = FileField('上传头像', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('上传')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已被使用，请换一个')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该邮箱已被使用，请换一个')


class RequestResetForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('请求重置密码')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('没有使用该邮箱的用户，你必须先注册')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置密码')
