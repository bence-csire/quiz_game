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


# class QuizForm(FlaskForm):
#     select_field = SelectField('Choose an option', choices=[("True", "True"), ("False", "False")])


class QuizForm(FlaskForm):
    question1 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    question2 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    question3 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    question4 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    # TODO: the answers should be the correct and incorrect answers from answer table in a random order
    question5 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    question6 = SelectField("question", choices=[("True", "True"), ("False", "False")])
    question7 = StringField(render_kw={"placeholder": "question"})
    question8 = StringField(render_kw={"placeholder": "question"})
    question9 = StringField(render_kw={"placeholder": "question"})
    question10 = StringField(render_kw={"placeholder": "question"})


# TODO: if all topics then choose from everywhere
# TODO: Check if it is possible to simplify it?
# TODO: Add function where admin user can submit quiz by giving question ID-s (not random)
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
    questions = [true_false_questions, single_choice_questions, short_answer_questions, numeric_questions]
    dict_ = question_dictionary(questions)
    return dict_


def question_dictionary(questions):
    question_dict = {}
    for list_ in questions:
        for q in list_:
            answer_id = database.Answer.query.filter_by(id=q.id).all()
            question_dict[q.id] = {
                "question": q.question,
                "answer": answer_id[0].correct_answer,
                "incorrect_answer": answer_id[0].incorrect_answer
            }
    return question_dict
