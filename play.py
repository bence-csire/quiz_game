from sqlalchemy import func

import database


# TODO: if all topics then choose from everywhere
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
