from flask import Flask, session, g
from flask_bootstrap import Bootstrap
from exts import mongo
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.reading import bp as read_bp
import config
from bson import ObjectId

#导入PDF阅读插件
ALLOW_EXTENSION = {'pdf'}

#启动Flask
app = Flask(__name__)
bootstrap = Bootstrap(app)

#启动mongodb
mongo.init_app(app, uri=config.MONGO_URI)

#导入Flask相关配置
app.config.from_object(config)

#导入蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(read_bp)


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


# 启动程序
if __name__ == '__main__':
    app.run()
