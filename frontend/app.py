import blueprints, models
import assets, jinja
from config import Config

from flask_login import LoginManager
from flask import Flask, flash, redirect, url_for

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    models.init_app(app)
    assets.init_app(app)
    jinja.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(blueprints.public.bp)
    app.register_blueprint(blueprints.habitat.bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauth_handler():
    flash("You must be logged in to view this page", "error")
    return redirect(url_for("public.login"))


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
