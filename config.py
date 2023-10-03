SECRET_KEY = "ashjbjhbce"

# 配置MongoDB数据库
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_DATABASE = 'acl_bibs'
MONGO_URI = 'mongodb://{0}:{1}/{2}'.format(MONGO_HOST, MONGO_PORT, MONGO_DATABASE)

# 配置PDF阅读器

# 上传路径
# todo:上传路径变得灵活，不要写死
UPLOAD_FOLDER = '/Users/ldbb/Desktop/flaskProject/static/uploads'
ALLOW_EXTENSION = {'pdf'}