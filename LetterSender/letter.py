from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

@app.route("/")
def login():
    return render_template("template/login.html")


@app.route("/login", methods = ["POST"])
def login_post():
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        return render_template("template/login.html")
    else:
        return "<h1>Errou</h1>"


app.run()
