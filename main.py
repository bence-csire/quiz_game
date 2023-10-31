# Import order. Is it okay like this?
# TODO: add requirements file
from flask import Flask, render_template, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

import database
import question
import quiz
import trivia
import users

# TODO: create an automatic job which gets questions from trivia. How many request can I make to TRIVIA a day?
#  How many questions should I take daily? 50-100?
# TODO: create a page where a user would be able to play the quiz

app = Flask(__name__)
# TODO: make it a real secret key
app.secret_key = "any-string-you-want-just-keep-it-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///questions.db"
database.init_app(app)
Bootstrap5(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    # TODO: query.get old, new one is session.get, make it work
    return database.User.query.get(int(user_id))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("index.html")


# TODO: make sure the added questions has the same string format (e.g Pascal or everything small)
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if current_user.admin:
        form = question.QuestionForm()
        if form.validate_on_submit():
            database.add_question(form.question.data, form.category.data, form.type_.data)
            new_question = database.Question.query.filter_by(question=form.question.data).first()
            database.add_answer(form.correct_answer.data, form.incorrect_answer.data, new_question.id)
            flash("Question submitted successfully!", "success")
            return redirect(url_for("add"))
        return render_template("add.html", form=form)
    else:
        return render_template("admin.html")


# TODO: add the login form to the users.py file
@app.route("/login", methods=["GET", "POST"])
def login():
    form = users.LoginForm()
    if form.validate_on_submit():
        user = database.User.query.filter_by(username=form.username.data).first()
        # TODO: popup for wrong username/password
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("choose_quiz"))
        flash("Wrong username or password. Please try again.", "error")
    return render_template("login.html", form=form)


# TODO: add the register form to the users.py file
@app.route("/register", methods=["GET", "POST"])
def register():
    form = users.RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = database.User(username=form.username.data, password=hashed_password, admin=form.admin.data)
        database.db.session.add(new_user)
        database.db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/quiz", methods=["GET", "POST"])
@login_required
def choose_quiz():
    form = quiz.QuizCategorySelection()
    if form.validate_on_submit():
        category = form.category.data
        questions_dict = quiz.create_quiz(category)
        session["questions_dict"] = questions_dict
        return redirect(url_for("play_quiz"))
    return render_template("quiz.html", form=form)


@app.route("/play", methods=["GET", "POST"])
@login_required
def play_quiz():
    questions_dictionary = session.get("questions_dict")
    form = quiz.QuizForm()
    return render_template("play.html", form=form, questions_dictionary=questions_dictionary)


with app.app_context():
    database.db.create_all()
    trivia.add()

if __name__ == "__main__":
    app.run()
