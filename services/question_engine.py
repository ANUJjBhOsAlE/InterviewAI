import json
import random


def load_questions():
    with open("data/questions.json", "r") as file:
        return json.load(file)


def get_questions(role, experience, difficulty, count=5):

    data = load_questions()

    questions = data[role][experience][difficulty]

    # Shuffle questions
    questions = questions.copy()
    random.shuffle(questions)

    return questions[:count]