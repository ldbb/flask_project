import wtforms
from exts import mongo
from wtforms.validators import Email, Length, EqualTo


# Forms:主要就是用来验证前端提交的数据是否符合要求
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])



class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])


    # 自定义验证
    # 邮箱是否已经被注册

    def validate_email(self, field):
        email = field.data
        user = mongo.db.user.find_one({"email": email})
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")


class ResetForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
