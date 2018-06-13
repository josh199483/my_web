from flask import Flask,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import UploadSet, configure_uploads, IMAGES


mysql = SQLAlchemy()
loginManager = LoginManager()
babel = Babel()
debug = DebugToolbarExtension()
imagesUpload = UploadSet('img', IMAGES) 
### 其他組態及設定(無法放到組態檔)
loginManager.session_protection = 'strong' # ['basic','None','strong'] 使用者修改 session的安全因應機制
loginManager.login_view = 'main.login' # 登入頁面的路徑



def create_app(config_name='production'):
    # instance_relative_config: 讀取 config檔的相對路徑, 由「application root path」改為「instance_path」
    apprun = Flask(__name__, instance_relative_config=True)
    
    ### 讀取 config.py 載入組態資訊
    from config import cfg
    apprun.config.from_object(cfg[config_name])
    cfg[config_name].init_app(apprun)

    ### 由 instance_path(預設為 "instance/")載入敏感資訊
    apprun.config.from_pyfile('secret.py')

    ### 初始化 extension
    mysql.init_app(apprun)
    loginManager.init_app(apprun)
    babel.init_app(apprun)
    debug.init_app(apprun)
    configure_uploads(apprun, imagesUpload)

    ### 註冊 blueprint
    register_blueprints(apprun)

    return apprun


# def initialize_extensions(app):
#     """
#     初始化 extension
#     """
#     ### 在app起始的時候，把以下的package都使用進去
#     mysql.init_app(app)
#     loginManager.init_app(app)
#     babel.init_app(app)

#     # from app.main.app import imagesUpload
#     # configure_uploads(app, imagesUpload)

#     if config_name == 'development':    # 若為'development'(開發模式), 則啟用開發工具套件 
#         toolbar = DebugToolbarExtension(app)


def register_blueprints(app):
    """
    註冊 blueprint
    """
    ### 這裡必須為了之後的 views 註冊 blueprint
    from .main import main 
    app.register_blueprint(main, url_prefix='/main')