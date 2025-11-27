from datetime import datetime
from typing import List, Tuple

from flask import Blueprint, flash, redirect, render_template, request, url_for, g, abort, make_response

from ..db import db
from ..models import Asset, Sizing
from .auth import login_required, get_current_user
from ..models.asset import round_to_thousands

sizing_bp = Blueprint("sizing", __name__)


def _parse_assets(form) -> List[Tuple[str, int, str]]:
    names = form.getlist("asset_name")
    quantities = form.getlist("asset_quantity")
    descriptions = form.getlist("asset_description")

    parsed = []
    for name, qty, desc in zip(names, quantities, descriptions):
        name = name.strip()
        desc = desc.strip()
        try:
            qty_int = int(qty) if qty else 0
        except ValueError:
            qty_int = 0

        qty_int = round_to_thousands(qty_int)
        if name and qty_int > 0:
            parsed.append((name, qty_int, desc))
    return parsed


def _get_user_sizing_or_404(sizing_id: int, user_company_id: int) -> Sizing:
    sizing = Sizing.query.filter_by(id=sizing_id, company_id=user_company_id).first()
    if not sizing:
        abort(404)
    return sizing


@sizing_bp.route("/sizings")
@login_required
def list_sizings():
    user = get_current_user()
    sizings = (
        Sizing.query.filter_by(company_id=user.company_id)
        .order_by(Sizing.created_at.desc())
        .all()
    )
    return render_template("sizing/index.html", sizings=sizings, user=user)


@sizing_bp.route("/sizings/new", methods=["GET", "POST"])
@login_required
def create_sizing():
    user = get_current_user()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        assets = _parse_assets(request.form)

        if not title:
            flash("Título é obrigatório.", "danger")
            return render_template("sizing/form.html", mode="create", assets=assets)

        if not assets:
            flash("Inclua pelo menos um ativo com quantidade válida.", "danger")
            return render_template("sizing/form.html", mode="create", assets=assets)

        sizing = Sizing(
            title=title,
            description=description,
            company_id=user.company_id,
            user_id=user.id,
            created_at=datetime.utcnow(),
        )
        db.session.add(sizing)
        db.session.flush()  # obtém ID para assets

        for name, qty, desc in assets:
            db.session.add(Asset(name=name, quantity=qty, description=desc, sizing_id=sizing.id))

        db.session.commit()
        flash("Sizing criado com sucesso.", "success")
        return redirect(url_for("sizing.list_sizings"))

    return render_template("sizing/form.html", mode="create", assets=[])


@sizing_bp.route("/sizings/<int:sizing_id>")
@login_required
def show_sizing(sizing_id: int):
    user = get_current_user()
    sizing = _get_user_sizing_or_404(sizing_id, user.company_id)
    return render_template("sizing/show.html", sizing=sizing, user=user)


@sizing_bp.route("/sizings/<int:sizing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_sizing(sizing_id: int):
    user = get_current_user()
    sizing = _get_user_sizing_or_404(sizing_id, user.company_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        assets = _parse_assets(request.form)

        if not title:
            flash("Título é obrigatório.", "danger")
            return render_template("sizing/form.html", mode="edit", sizing=sizing, assets=assets)

        sizing.title = title
        sizing.description = description

        # Atualiza assets removendo anteriores e recriando baseado no form
        sizing.assets.clear()
        db.session.flush()
        for name, qty, desc in assets:
            sizing.assets.append(Asset(name=name, quantity=qty, description=desc))

        db.session.commit()
        flash("Sizing atualizado.", "success")
        return redirect(url_for("sizing.show_sizing", sizing_id=sizing.id))

    assets = [(a.name, a.quantity, a.description or "") for a in sizing.assets]
    return render_template("sizing/form.html", mode="edit", sizing=sizing, assets=assets)


@sizing_bp.route("/sizings/<int:sizing_id>/delete", methods=["POST"])
@login_required
def delete_sizing(sizing_id: int):
    user = get_current_user()
    sizing = _get_user_sizing_or_404(sizing_id, user.company_id)
    db.session.delete(sizing)
    db.session.commit()
    flash("Sizing removido.", "info")
    return redirect(url_for("sizing.list_sizings"))


@sizing_bp.route("/sizings/<int:sizing_id>/export")
@login_required
def export_sizing(sizing_id: int):
    user = get_current_user()
    sizing = _get_user_sizing_or_404(sizing_id, user.company_id)
    response = make_response(render_template("sizing/export.html", sizing=sizing, user=user))
    response.headers["Content-Disposition"] = f'attachment; filename="sizing-{sizing.id}.html"'
    response.headers["Content-Type"] = "text/html"
    return response
