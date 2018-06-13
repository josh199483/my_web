"""
建立時間: 2018
作者: Joshua
說明:
    登入機制
"""

from flask_wtf import FlaskForm  #Form rename to FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
# from .app import imagesUpload
from .models import User
from .. import imagesUpload

# 登入表單
class LoginForm(FlaskForm):
    user_name = StringField('UserName',validators=[Required(message='帳號不能是空的'),Length(1,64)])
    password = PasswordField('Password',validators=[Required(message='密碼不能是空的')])
    submit = SubmitField('Log in')


# 註冊表單
# class RegistrationForm(FlaskForm):
#     email = StringField('Email',validators=[Required(),Length(1,64),Email()])
#     user_name = StringField('Username',validators=[
#         Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'error')])
#     password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='確認密碼與密碼一致')])
#     password2 = PasswordField('confirm password',validators=[Required()])
#     submit = SubmitField('register')

    # def validate_email(self,field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email 已經存在')
    # def validate_username(self,field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('username 已經存在')


# 上傳圖片表單
class ImageForm(FlaskForm):
    uploads = FileField('uploads', validators=[
        FileAllowed(imagesUpload, '只能放圖片喔!'),
        FileRequired('請放一張圖片!')
    ])
    submit = SubmitField('Upload_IMG')