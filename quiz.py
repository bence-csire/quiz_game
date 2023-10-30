from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from sqlalchemy import func

import database


class QuizCategorySelection(FlaskForm):
    category = SelectField("Category", choices=[("All topics", "All topics"),
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


class QuizForm(FlaskForm):
    answer1 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    answer2 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    answer3 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    answer4 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    # TODO: the answers should be the correct and incorrect answers from answer table in a random order
    answer5 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    answer6 = SelectField("Answer", choices=[("True", "True"), ("False", "False")])
    answer7 = StringField(render_kw={"placeholder": "Answer7"})
    answer8 = StringField(render_kw={"placeholder": "Answer8"})
    answer9 = StringField(render_kw={"placeholder": "Answer9"})
    answer10 = StringField(render_kw={"placeholder": "Answer10"})


# TODO: if all topics then choose from everywhere
# TODO: Check if it is possible to simplify it?
# TODO: Admin user can submit quiz by giving question ID-s (not random)
# TODO: Create a list with the answers
def create_quiz(category):
    true_false_questions = database.db.session.query(database.Question).filter(database.Question.q_category == category,
                                                                               database.Question.type == "boolean").order_by(
        func.random()).distinct(database.Question.id).limit(4).all()
    single_choice_questions = database.db.session.query(database.Question).filter(
        database.Question.q_category == category, database.Question.type == "single choice").order_by(
        func.random()).distinct(database.Question.id).limit(2).all()
    short_answer_questions = database.db.session.query(database.Question).filter(
        database.Question.q_category == category,
        database.Question.type == "short answer").order_by(func.random()).distinct(database.Question.id).limit(2).all()
    numeric_questions = database.db.session.query(database.Question).filter(database.Question.q_category == category,
                                                                            database.Question.type == "numeric").order_by(
        func.random()).distinct(database.Question.id).limit(2).all()
    new_quiz = database.Quiz(category, True, true_false_questions[0].id, true_false_questions[1].id,
                             true_false_questions[2].id, true_false_questions[3].id, single_choice_questions[0].id,
                             single_choice_questions[1].id, short_answer_questions[0].id, short_answer_questions[1].id,
                             numeric_questions[0].id, numeric_questions[1].id)
    database.db.session.add(new_quiz)
    database.db.session.commit()
    return true_false_questions, single_choice_questions, short_answer_questions, numeric_questions
