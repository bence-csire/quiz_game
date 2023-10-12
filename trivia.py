import database
import sqlalchemy
import requests
import html

parameters = {
    "amount": 10,
    "type": "boolean",
}


response = requests.get("https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
data = response.json()
question_data = data["results"]


def add():
    for item in question_data:
        try:
            decoded_question = html.unescape(item["question"])
            database.add_question(decoded_question, item["category"], item["type"])
            new_question = database.Question.query.filter_by(question=decoded_question).first()
            # TODO: add multiple incorrect answer, not only one
            print(type(item["incorrect_answers"][0]))
            database.add_answer(item["correct_answer"], item["incorrect_answers"][0], new_question.id)
        except sqlalchemy.exc.IntegrityError:
            database.db.session.rollback()
