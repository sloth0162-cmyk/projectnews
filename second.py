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

@second.route("/indianmarket")
def indianmarket():
    return render_template("secondpage/indianmarket.html")

@second.route("/realestate")
def real_estate():
    return render_template("secondpage/realestate.html")

@second.route("/commodities")
def commodities():
    return render_template("secondpage/commodities.html")
@second.route("/tech")
def tech():
    return render_template("secondpage/tech.html")

@second.route("/stockmarket")
def stockmarket():
    return render_template("secondpage/stockmarket.html")