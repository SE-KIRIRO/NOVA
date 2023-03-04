from . import main
from flask import render_template, session, redirect, url_for, flash, current_app
from datetime import datetime
from .forms import NameForm
from ..models import User, Role
from ..email import send_email
from .. import db


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
    return render_template("index.html",
                           current_time=datetime.utcnow(), name= session.get("name"),
                           form=form , known=session.get("known", False))


@main.route("/user<name>")
def user(name):
    return render_template("user.html", name=name)