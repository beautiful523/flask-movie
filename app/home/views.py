# coding:utf8
import datetime
import uuid
from functools import wraps

import os
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db, app, rd
from app.home.forms import RegisterForm, LoginForm, UserDetailForm, PwdForm, CommentForm
from app.models import User, UserLog, Preview, Tag, Movie, Comment, Moviecol
from . import home
from flask import render_template, redirect, url_for, flash, session, request, Response
import json


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)  # 分割文件名
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]  # 新组合的文件名
    return filename


@home.route("/<int:page>/", methods=["GET"])
def index(page):
    tags = Tag.query.all()
    tid = request.args.get("tid", 0)
    page_data = Movie.query
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))
    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))
    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    pm = request.args.get("pm", 0)
    if int(pm) == 1:
        page_data = page_data.order_by(
            Movie.playnum.desc()
        )
    if int(pm) == 2:
        page_data = page_data.order_by(
            Movie.playnum.asc()
        )

    cm = request.args.get("cm", 0)
    if int(cm) == 1:
        page_data = page_data.order_by(
            Movie.commentnum.desc()
        )
    if int(cm) == 2:
        page_data = page_data.order_by(
            Movie.commentnum.asc()
        )
    if page is None:
        page = 1
    page = request.args.get("page", 1)
    page_data = page_data.paginate(page=int(page), per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data)


@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user is None:
            flash("昵称不存在", 'err')
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["pwd"]):
            flash("密码错误", 'err')
            return render_template('home/login.html', form=form)
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = UserLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(request.args.get("next") or url_for("home.user"))
    return render_template('home/login.html', form=form)


@home.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    return render_template('home/register.html', form=form)


@home.route("/logout/", methods=["GET"])
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    return redirect(url_for('home.login'))  # 参数是视图


# 会员中心
@home.route("/user/", methods=["GET", "POST"])
@admin_login_req
def user():
    form = UserDetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        if form.face.data:  # 如果表单中添加了头像图片
            file_face = secure_filename(form.face.data.filename)
            user.face = change_filename(file_face)  # 修改图片文件名
            if not os.path.exists(app.config["FC_DIR"]):  # 新建存储路径
                os.makedirs(app.config["FC_DIR"])
                os.chmod(app.config["FC_DIR"], 0o777)
            form.face.data.save(app.config["FC_DIR"] + user.face)  # 存储到目录
        name_count = User.query.filter_by(name=data["name"]).count()
        if data["name"] != user.name and name_count == 1:
            flash("昵称已经存在", "err")
            return render_template('home/user.html', form=form, user=user)
        email_count = User.query.filter_by(email=data["email"]).count()
        if data["email"] != user.email and email_count == 1:
            flash("邮箱已经存在", "err")
            return redirect(url_for("home.user"))
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if data["phone"] != user.phone and phone_count == 1:
            flash("电话号码已经存在", "err")
            return redirect(url_for("home.user"))
        user.name = data["name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for("home.user"))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@home.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(
            name=session["user"]
        ).first()
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码错误", "err")
            return redirect(url_for("home.pwd"))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功,请重新登录", "ok")
        return redirect(url_for("home.logout"))
    return render_template('home/pwd.html', form=form)


# 评论
@home.route("/comments/<int:page>/", methods=["GET"])
@admin_login_req
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == session["user_id"]
    ).order_by(
        Comment.addtime.desc()
    ).paginate(
        page=page, per_page=10
    )
    return render_template('home/comments.html', page_data=page_data)


# 登录日志
@home.route("/loginlog/<int:page>/", methods=["GET"])
@admin_login_req
def loginlog(page):
    if page is None:
        page = 1
    page_data = UserLog.query.join(User).filter(
        User.id == int(session["user_id"]),
    ).order_by(
        UserLog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 添加电影收藏
@home.route("/moviecol/add/", methods=["GET"])
@admin_login_req
def moviecol_add():
    mid = request.args.get("mid", "")
    uid = request.args.get("uid", "")
    moviecol = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid),
    ).count()
    if moviecol == 1:
        data = dict(ok=0)
    if moviecol == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid),
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    return json.dumps(data)


# 电影收藏
@home.route("/moviecol/<int:page>/")
@admin_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(User).join(Movie).filter(
        Movie.id == Moviecol.movie_id,
        User.id == session["user_id"]
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', page_data=page_data)


# 动画
@home.route("/animation/")
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


# 搜索
@home.route("/search/<int:page>")
def search(page):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    movie_count = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(
        page=page, per_page=10
    )
    page_data.key = key
    return render_template('home/search.html', key=key, page_data=page_data, movie_count=movie_count)


# 播放
@home.route("/play/<int:id>/<int:page>/", methods=["GET", "POST"])
def play(id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()

    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(
        page=page, per_page=10
    )

    if request.method == "GET":
        movie.playnum = movie.playnum + 1
        db.session.add(movie)
        db.session.commit()
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        movie.commentnum = movie.commentnum + 1
        db.session.add(comment)
        db.session.commit()
        flash("添加评论成功", "ok")
        return redirect(url_for("home.video", id=movie.id, page=1))
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data)


# 播放
@home.route("/video/<int:id>/<int:page>/", methods=["GET", "POST"])
def video(id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()

    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == movie.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(
        page=page, per_page=10
    )

    if request.method == "GET":
        movie.playnum = movie.playnum + 1
        db.session.add(movie)
        db.session.commit()
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            movie_id=movie.id,
            user_id=session["user_id"]
        )
        movie.commentnum = movie.commentnum + 1
        db.session.add(comment)
        db.session.commit()
        flash("添加评论成功", "ok")
        return redirect(url_for("home.video", id=movie.id, page=1))
    return render_template('home/video.html', movie=movie, form=form, page_data=page_data)


@home.route("/tm/", methods=["GET", "POST"])
def tm():
    if request.method == "GET":
        # 获取弹幕
        id = request.args.get("id")
        key = "movie" + str(id)
        if rd.llen(key):
            # 获取键值对应的数据，从第0条开始，获取2999条
            msgs = rd.lrange(key, 0, 2999)
            res = {
                "code": 1,
                "danmaku": [json.loads(v) for v in msgs]
            }
        else:
            res = {
                "code": 1,
                "danmaku": []
            }
        resp = json.dumps(res)

    if request.method == "POST":
        # 添加弹幕
        data = json.loads(request.get_data())
        msg = {
            "__v": 0,
            "author": data["author"],
            "time": data["time"],
            "text": data["text"],
            "color": data["color"],
            "type": data["type"],
            "ip": request.remote_addr,
            "_id": datetime.datetime.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex,
            "player": [
                data["player"]
            ]
        }
        res = {
            "code": 1,
            "data": msg
        }
        resp = json.dumps(res)
        rd.lpush("movie" + str(data["player"]), json.dumps(msg))
    return Response(resp, mimetype="application/json")