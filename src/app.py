from manager import login_manager
from config import Config

import blueprints, models
import assets, jinja

from flask import Flask


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


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )
