# TODO: check the correct order for imports
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask
from flask_bootstrap import Bootstrap5
import database
import trivia
# from flask_sqlalchemy import SQLAlchemy

# TODO: Create and access DB. TODO: Get questions from TRIVIA and add it to my DB. How many request can I make to
#   TRIVIA a day? How many questions should I take daily? 50-100?
# TODO: Create a form where an "admin" can submit questions (they have to be logged in) (what type of questions).
#   Save this questions into DB.
# TODO: Create a page where a user would be able to play the quiz

app = Flask(__name__)
# TODO: make it a real secret key
app.secret_key = "any-string-you-want-just-keep-it-secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///questions.db"
database.init_app(app)
Bootstrap5(app)


class QuestionForm(FlaskForm):
    type_ = SelectField(u"Type", choices=[("True/False", "True/False"),
                                          ("Single Choice", "Single Choice"),
                                          ("Short Answer", "Short Answer"),
                                          ("Numeric", "Numeric")], validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    category = SelectField(u"Category", choices=[("General Knowledge", "General Knowledge"),
                                                 ("Entertainment: Books", "Entertainment: Books"),
                                                 ("Entertainment: Film", "Entertainment: Film"),
                                                 ("Entertainment: Music", "Entertainment: Music"),
                                                 ("Entertainment: Musicals & Theatres", "Entertainment: Musicals & Theatres"),
                                                 ("Entertainment: Television", "Entertainment: Television"),
                                                 ("Entertainment: Video Games", "Entertainment: Video Games"),
                                                 ("Entertainment: Board Games", "Entertainment: Board Games"),
                                                 ("Science & Nature", "Science & Nature"),
                                                 ("Science: Computers", "Science: Computers"),
                                                 ("Science: Mathematics", "Science: Mathematics"),
                                                 ("Mythology", "Mythology"),
                                                 ("Sports", "Sports"),
                                                 ("Geography", "Geography"),
                                                 ("History", "History"),
                                                 ("Politics", "Politics"),
                                                 ("Art", "Art"),
                                                 ("Celebrities", "Celebrities"),
                                                 ("Animals", "Animals")],
                           validators=[DataRequired()])
    correct_answer = StringField("Correct Answer", validators=[DataRequired()])
    incorrect_answer = StringField("Wrong Answers (comma separated)")
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = QuestionForm()
    if form.validate_on_submit():
        database.add_question(form.question.data, form.category.data, form.type_.data)
        new_question = database.Question.query.filter_by(question=form.question.data).first()
        database.add_answer(form.correct_answer.data, form.incorrect_answer.data, new_question.id)
        return render_template("index.html")
    return render_template("add.html", form=form)


with app.app_context():
    database.db.create_all()
    trivia.add()

if __name__ == "__main__":
    app.run()
