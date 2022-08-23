from flask import Blueprint, render_template, request
from flask_login import login_user, login_required
from wtforms import FloatField, TimeField

import plotly.express as px
import pandas as pd
import plotly

from datetime import datetime, time
from habitat_tools import APITools
import json

from forms import ConfigForm, ReadingForm

bp = Blueprint("habitat", __name__, url_prefix="/habitat")
api_tools = APITools()


@bp.route("/")
def home():
    reading = api_tools.get_reading()

    context = {"page": "habitat", "reading": reading}
    return render_template("habitat.html", **context)


@bp.route("/readings", methods=["GET", "POST"])
def readings():
    habi_graph = None
    form = ReadingForm()
    if form.validate_on_submit():
        data = form.data
        readings = api_tools.filter_readings(unit=data["unit"], period=data["time"])
        data = {
            "Time": [r["time"] for r in readings],
            "Temperature": [float(r["temperature"]) for r in readings],
            "Humidity": [float(r["humidity"]) for r in readings],
        }
        df = pd.DataFrame(data)
        fig = px.line(
            df,
            x="Time",
            y=["Temperature", "Humidity"],
            title="Habitat Conditions",
        )
        fig = fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            width=1400,
            height=500,
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(111, 117, 128, .3)",
            title_font_size=25,
            title_font={"family": "Josefin Sans"},
            modebar={"bgcolor": "rgba(236, 236, 236, 1)"},
        )
        habi_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "page": "habitat",
        "content": "reading",
        "form": form,
        "habitat_graph": habi_graph,
    }
    return render_template("readings.html", **context)


@bp.route("/config", methods=["GET", "POST"])
@login_required
def config():
    form = ConfigForm(request.form or None)
    if form.validate_on_submit():
        data = {
            field.name: field.data
            for field in form._fields.values()
            if type(field) in (FloatField, TimeField)
        }
        resp = api_tools.set_config(data)

    config = api_tools.get_config()
    if config.get("error"):
        config = api_tools.new_config()
    form.populate_form(config)

    context = {"page": "habitat", "content": "config", "form": form}
    return render_template("config.html", **context)


@bp.route("/stats", methods=["GET"])
def stats():
    stats = api_tools.get_stats()

    context = {"page": "habitat", "content": "stats", "stats": stats}
    return render_template("stats.html", **context)
