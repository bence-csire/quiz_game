from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


# creating tables
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), unique=True, nullable=False)
    q_category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    # relationship
    answers = db.relationship("Answer", backref="question", cascade="all, delete-orphan")

    def __init__(self, question, q_category, type_):
        self.question = question
        self.q_category = q_category
        self.type = type_


def add_question(question, q_category, type_):
    q = Question(question, q_category, type_)
    db.session.add(q)
    db.session.commit()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correct_answer = db.Column(db.String(100), nullable=False)
    incorrect_answer = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))

    def __init__(self, correct_answer, incorrect_answer, question_id):
        self.correct_answer = correct_answer
        self.incorrect_answer = incorrect_answer
        self.question_id = question_id


def add_answer(correct_answer, incorrect_answer, question_id):
    a = Answer(correct_answer, incorrect_answer, question_id)
    db.session.add(a)
    db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    # TODO: store as a hash or other secure way
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    # relationship
    quiz = db.relationship("Quiz", backref="user")
    answered_quiz = db.relationship("AnsweredQuiz", backref="user")

    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.admin = admin


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    random = db.Column(db.Boolean, nullable=False)
    # Should it be ID or Question? How can I call it?
    question1 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question2 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question3 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question4 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question5 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question6 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question7 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question8 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question9 = db.Column(db.Integer, db.ForeignKey("question.id"))
    question10 = db.Column(db.Integer, db.ForeignKey("question.id"))
    userid = db.Column(db.String(100), db.ForeignKey("user.id"))


class AnsweredQuiz(db.Model):
    rating = db.Column(db.Integer)
    score = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.String(100), db.ForeignKey("user.id"), primary_key=True)
    quizid = db.Column(db.Integer, db.ForeignKey("quiz.id"), primary_key=True)
    # category = db.Column(db.String(100), nullable=False)
