from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


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
                                                 ("Entertainment: Musicals & Theatres",
                                                  "Entertainment: Musicals & Theatres"),
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