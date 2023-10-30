from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class QuizForm(FlaskForm):
    category = SelectField(u"Category", choices=[("All topics", "All topics"),
                                                 ("General Knowledge", "General Knowledge"),
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
    submit = SubmitField("Submit")
