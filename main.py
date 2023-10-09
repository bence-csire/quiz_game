# todo check the correct order for imports
# from question_model import Question
# from data import question_data
# from quiz_brain import QuizBrain
# from ui import QuizInterface
# import requests
from flask import Flask
import database
import trivia
# from flask_sqlalchemy import SQLAlchemy

# TODO Create and access DB.
# TODO Get questions from TRIVIA and add it to my DB. How many request can I make to TRIVIA a day? How many questions should I take daily? 50-100?
# TODO Create a form where an "admin" can submit questions (they have to be logged in) (what type of questions). Save this questions into DB.
# TODO Create a page where a user would be able to play the quiz

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///questions.db"
database.init_app(app)
with app.app_context():
    database.db.create_all()

    trivia.add_question()
