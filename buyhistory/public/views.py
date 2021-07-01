# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import re

from flask import (
    Blueprint,
    current_app,
    flash,
    render_template,
    request,
    send_from_directory,
)
from flask.helpers import url_for
from werkzeug.utils import redirect

from buyhistory.utils import flash_errors

from .forms import QueryForm

blueprint = Blueprint("public", __name__, static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = QueryForm()
    current_app.logger.info("Hello from the home page!")
    if request.method == "POST":
        if form.validate_on_submit():
            address = form.address.data
            res = re.search(r"amazon.(\S{2,6})/\S{1,4}/(\w+)", address)
            try:
                domain = res.group(1)
                asin = res.group(2)
                return redirect(
                    url_for(
                        "public.result", domain=domain, asin=asin, range=form.range.data
                    )
                )
            except:
                flash("Please check your Amazon address!", "danger")
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/res/<asin>/")
def result(asin, range="90"):
    form = QueryForm()
    domain = request.args.get("domain", "com")
    range = request.args.get("range", "90")
    return render_template(
        "public/results.html", form=form, domain=domain, asin=asin, range=range
    )


@blueprint.route("/about/")
def about():
    """About page."""
    return render_template("public/about.html")


@blueprint.route("/favicon.ico")
def favicon():
    return send_from_directory("./static/build/img", "favicon.ico")
