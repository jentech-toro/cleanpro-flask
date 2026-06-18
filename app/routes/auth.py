from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
import os

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        valid_username = username == os.getenv("ADMIN_USERNAME", "admin")
        valid_password = check_password_hash(os.getenv("ADMIN_PASSWORD_HASH", ""), password)

        if valid_username and valid_password:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))

        return render_template("login.html", error="Usuario o contraseña incorrectos")

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("public.home"))
