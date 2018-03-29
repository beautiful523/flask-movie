# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"请输入昵称")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"请输入邮箱"),
            Email('邮箱格式不正确')
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
        }
    )
    phone = StringField(
        label=u"手机",
        validators=[
            DataRequired(u"请输入手机"),
            Regexp("1[3458]\\d{9}$", message='手机格式不正确')
        ],
        description=u"手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入密码")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
        }
    )
    repwd = PasswordField(
        label=u"确认密码",
        validators=[
            DataRequired(u"请输入确认密码"),
            EqualTo('pwd', "两次密码不一致")

        ],
        description=u"确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码",
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name)
        if user.count() != 0:
            raise ValidationError("昵称已经存在")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email)
        if user.count() != 0:
            raise ValidationError("邮箱已经存在")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone)
        if user.count() != 0:
            raise ValidationError("手机号码已经存在")


class LoginForm(FlaskForm):
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"请输入昵称")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入密码")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )


class UserDetailForm(FlaskForm):
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"请输入昵称")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入昵称",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"请输入邮箱"),
            Email('邮箱格式不正确')
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱",
        }
    )
    phone = StringField(
        label=u"手机",
        validators=[
            DataRequired(u"请输入手机"),
            Regexp("1[3458]\\d{9}$", message='手机格式不正确')
        ],
        description=u"手机",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机",
        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像")
        ],
        description="头像",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control", "rows": "10"}
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-success",
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label=u"旧密码",
        validators=[
            DataRequired(u"请输入旧密码")
        ],
        description=u"旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
        }
    )
    new_pwd = PasswordField(
        label=u"新密码",
        validators=[
            DataRequired(u"请输入新密码")
        ],
        description=u"新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            "class": "btn-success",
        }

    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["user"]
        user = User.query.filter_by(
            name=name
        ).first()  # 这里是根据session的用户名查找，所以注册的时候不能重名
        if not user.check_pwd(pwd):
            raise ValidationError("旧密码错误")


class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请输入内容")
        ],
        description="内容",
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )