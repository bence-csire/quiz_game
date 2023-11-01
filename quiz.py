from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
from sqlalchemy import func

import database


class QuizCategorySelection(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("All topics", "All topics"),
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
    submit = SubmitField("Submit")

# class QuizQuestion(SelectField):
#     question = SelectField()
#
#
#     def __init__(self, questions_dict):
#         super(QuizForm, self).__init__()
#         # self.questions.choices = [("True", "True")]
#         print(questions_dict)


class QuizForm(FlaskForm):

    questions = SelectField()
    # question_list = QuizQuestion[]

    def __init__(self, questions_dict):
        super(QuizForm, self).__init__()
        # self.questions.choices = [("True", "True")]
        for key, value in questions_dict.items():
            self.questions.name = [value["question"]]
            self.questions.choices = [value["correct_answer"]]
        print(questions_dict)


        # for key, value in questions_dict.items():
        #     question = SelectField(value["question"], choices=[("True", "True"), ("False", "False")])
        #     self.questions.append(question)


# class QuizForm(FlaskForm):
#     question_true_false = SelectField(choices=[("True", "True"), ("False", "False")])
    # question_single_choice = SelectField("question", choices=[("True", "True"), ("False", "False")])
    # question_short_answer = StringField(render_kw={"placeholder": "question"})
    # question_numeric = StringField(render_kw={"placeholder": "question"})
    # # TODO: the answers should be the correct and incorrect answers from answer table in a random order



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
    i = 0
    for list_ in questions:
        for q in list_:
            answer_id = database.Answer.query.filter_by(id=q.id).all()
            question_dict[i] = {
                "question": q.question,
                "correct_answer": answer_id[0].correct_answer,
                "incorrect_answer": answer_id[0].incorrect_answer
            }
            i += 1
    print(question_dict)
    return question_dict
