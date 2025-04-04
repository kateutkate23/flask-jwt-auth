from flask import Flask
import redis
from .config import Config


class App(Flask):
    redis: redis.Redis


def create_app() -> App:
    app = App(__name__)
    app.config.from_object(Config)

    app.redis = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB']
    )

    try:
        app.redis.ping()
        print("redis is working")
    except redis.ConnectionError:
        print("cannot connect to redis")

    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
