#/backend/app/__init__.py
from flask import Flask
from .routes import main
from .db import init_db

def create_app():
    app = Flask(
        __name__,
        template_folder="/app/templates",     # 模板路径
        static_folder="/app/static",        # 静态文件路径
        static_url_path="/static"                   # 使 /styles.css 能直接访问
    )
    app.register_blueprint(main)
    init_db()
    return app
