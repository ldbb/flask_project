from flask import request, Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mongo
from blueprints.forms import RegisterForm, LoginForm, ResetForm
from werkzeug.security import generate_password_hash, check_password_hash


# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = {"email": str(email), "username": str(username), "password": generate_password_hash(password)}
            mongo.db.user.insert_one(user)
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

@bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = mongo.db.user.find_one({"email": email})
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user["password"], password):
                # cookie：
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = str(user["_id"])
                return redirect("/")
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    else:
        form = ResetForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = mongo.db.user.find_one({"email": email})
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.reset_password"))
            else:
                mongo.db.user.update_one({"email": email}, {"$set": {"password": generate_password_hash(password)}})
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.reset_password"))




