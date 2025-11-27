from typing import Callable, Optional

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    flash,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import db
from ..models import User, Company

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_current_user() -> Optional[User]:
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def load_logged_in_user():
    g.user = get_current_user()


def login_required(view: Callable):
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Faça login para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        company_name = request.form.get("company", "").strip()

        errors = []
        if not name:
            errors.append("Nome é obrigatório.")
        if not email:
            errors.append("Email é obrigatório.")
        if not password:
            errors.append("Senha é obrigatória.")
        if not company_name:
            errors.append("Empresa é obrigatória.")

        if User.query.filter_by(email=email).first():
            errors.append("Email já cadastrado.")

        if errors:
            for msg in errors:
                flash(msg, "danger")
            return render_template("auth/signup.html")

        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
            db.session.flush()

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            company=company,
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash("Cadastro realizado com sucesso.", "success")
        return redirect(url_for("sizing.list_sizings"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Credenciais inválidas.", "danger")
            return render_template("auth/login.html")

        session["user_id"] = user.id
        flash("Login realizado.", "success")
        return redirect(url_for("sizing.list_sizings"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("auth.login"))
