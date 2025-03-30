from flask import Flask
import redis
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])
    try:
        app.redis.ping()
        print("Redis подключен успешно!")
    except redis.ConnectionError:
        print("Не удалось подключиться к Redis")
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app
