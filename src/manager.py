from models import User

from flask_login import LoginManager
from flask import Flask, flash, redirect, url_for

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return user
    return None


@login_manager.unauthorized_handler
def unauth_handler():
    flash("You must be logged in to view this page", "error")
    return redirect(url_for("public.login"))
