from flask import Flask, render_template
from endpoints import api_bp


app = Flask(__name__)


app.register_blueprint(api_bp)


@app.get("/")
def read_root():
    return render_template("user.html")


@app.get("/admin")
def read_admin():
    return render_template("admin.html")


@app.get("/user")
def read_user():
    return render_template("user.html")
