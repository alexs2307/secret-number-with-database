import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from sqla_wrapper import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy("sqlite:///db.sqlite")
class Secret_Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    secret_number = db.Column(db.Integer, unique=False)
    secret_password = db.Column(db.String, unique=True)

db.create_all()


@app.route("/", methods=["GET"])
def index():
    if request.cookies.get("secret_password"):
        user = db.query(Secret_Number).filter_by(secret_password=request.cookies.get("secret_password")).first()
    else:
        user = None
    return render_template("index.html", user=user)

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
        secret_number = random.randint(1, 30)
        user = db.query(Secret_Number).filter_by(secret_password=request.form.get("user-password")).first()
        if not user:
            user = Secret_Number(name=request.form.get("user-name"),
                                 secret_password=request.form.get("user-password"),
                                 secret_number=secret_number)
            user.save()
        response = make_response(redirect(url_for('index')))
        response.set_cookie("secret_password", request.form.get("user-password"))


        return response
@app.route("/result", methods=["POST"])
def result():
    guessing = int(request.form.get("guessing"))
    user = db.query(Secret_Number).filter_by(secret_password=request.cookies.get("secret_password")).first()
    if guessing == user.secret_number:
        message = f"Bingo! The secret number is {guessing}."
        user.secret_number = random.randint(1, 30)
        user.save()
    elif guessing > user.secret_number:
        message = "Your wrong! Try something smaller."
    elif guessing < user.secret_number:
        message = "Your wrong! Try something bigger."

    return render_template("result.html", message=message)

if __name__ == '__main__':
    app.run(use_reloader=True)  # if you use the port parameter, delete it before deploying to Heroku