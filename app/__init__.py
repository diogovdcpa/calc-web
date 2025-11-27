from flask import Flask, redirect, url_for

from .db import db
from .settings import get_settings
from .controllers.auth import auth_bp, load_logged_in_user
from .controllers.sizing import sizing_bp


def create_app() -> Flask:
    """
    App factory para a plataforma CalcWeb.
    Configura SQLAlchemy, registra blueprints e cria o schema básico.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    settings = get_settings()
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = settings.secret_key

    db.init_app(app)

    # Importa modelos antes de criar tabelas
    from . import models  # noqa: WPS433,F401

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(sizing_bp)

    # Rota raiz: encaminha para listagem de sizings
    @app.route("/")
    def home():
        return redirect(url_for("sizing.list_sizings"))

    # Carrega usuário na requisição (g.user)
    app.before_request(load_logged_in_user)

    return app
