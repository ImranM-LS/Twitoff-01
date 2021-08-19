import os
from flask import Flask, render_template, request, redirect
from .models import db, User, Tweet
import re

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()  

    @app.route("/", methods=["GET", "POST"])
    def home():
        name = request.form.get("name")
        text = request.form.get("text")
        userid = request.form.get("userid")

        if name:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()

        if (text and userid):
            tweet = Tweet(text=text, user_id=userid)
            db.session.add(tweet)
            db.session.commit()

        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template("home.html", users=users, tweets=tweets)

    @app.route("/delete", methods=["POST"])
    def delete():
        name = request.form.get("name")
        text = request.form.get("text")

        if name:
            user = User.query.filter_by(name=name).first()
            db.session.delete(user)
            db.session.commit()

        if text:
            tweet = Tweet.query.filter_by(text=text).first()
            db.session.delete(tweet)
            db.session.commit()

        return redirect("/")

    @app.route('/iris')
    def iris():    
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial').fit(X, y)

        return str(clf.predict(X[:2, :]))

    return app
