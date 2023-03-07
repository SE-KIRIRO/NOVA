from . import main
from flask import render_template, session, redirect, url_for, flash, current_app
from datetime import datetime
from .forms import NameForm
from ..models import User, Role, Permission
from ..email import send_email
from .. import db
from flask_login import current_user, login_required
from ..decorators import admin_required, permission_required


@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            if current_app.config["NOVA_ADMIN"]:
                send_email(current_app.config["NOVA_ADMIN"], "NEW user", 
                           "mail/new_user", user=user)
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("main.index"))
    return render_template("index.html",
                           current_time=datetime.utcnow(), name= session.get("name"),
                           form=form , known=session.get("known", False))


@main.route("/user<name>")
def user(name):
    return render_template("user.html", name=name)

@main.route("/admin")
@login_required
@admin_required
def for_admins_only():
    return "for administrators"

@main.route("/moderate")
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "for comment moderators"