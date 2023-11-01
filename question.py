from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    type_ = SelectField(
        "Type",
        choices=[
            ("boolean", "True/False"),
            ("single choice", "Single Choice"),
            ("short answer", "Short Answer"),
            ("numeric", "Numeric")
        ],
        validators=[DataRequired()]
    )
    question = StringField("Question", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("General Knowledge", "General Knowledge"),
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
            ("Animals", "Animals")
        ],
        validators=[DataRequired()]
    )
    correct_answer = StringField("Correct Answer", validators=[DataRequired()])
    incorrect_answer = StringField("Wrong Answers (comma separated)")
    submit = SubmitField("Submit")
