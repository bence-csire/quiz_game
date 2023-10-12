# TODO: check the correct order for imports
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask import Flask
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


class QuestionForm(FlaskForm):
    type_ = SelectField(u"type", choices=[("True/False", "True/False"),
                                          ("Single Choice", "Single Choice"),
                                          ("Short Answer", "Short Answer"),
                                          ("Numeric", "Numeric")], validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    category = SelectField(u"category", choices=[("General Knowledge", "General Knowledge"),
                                                 ("Entertainment: Books", "Entertainment: Books"),
                                                 ("Entertainment: Film", "Entertainment: Film")],
                           validators=[DataRequired()])
    correct_answer = StringField("Correct Answer", validators=[DataRequired()])
    wrong_answer = StringField("Wrong Answers (comma separated)")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = QuestionForm()
    if form.validate_on_submit():
        print(f"\n{form.type_.data}, {form.question.data}")
    return render_template("add.html", form=form)


with app.app_context():
    database.db.create_all()
    trivia.add()

if __name__ == "__main__":
    app.run(debug=True)
