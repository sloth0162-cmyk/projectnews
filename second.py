from flask import Blueprint, render_template

second = Blueprint("second", __name__)
@second.route("/crypto")
def crypto():
    return render_template("secondpage/crypto.html")

@second.route("/business")
def business():
    return render_template("secondpage/business.html")

@second.route("/about")
def about():
    return render_template("secondpage/about.html")