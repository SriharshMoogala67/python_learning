import random


class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

    def display(self):
        print(self.text)

        for option in self.options:
            print(option)

    def check_answer(self, answer):
        return answer.upper() == self.correct_answer.upper()


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def get_user_answer(self):
        while True:
            answer = input("Enter A, B, C, or D: ").upper()

            if answer in ["A", "B", "C", "D"]:
                return answer

            print("Invalid answer")

    def start(self):
        self.score = 0

        random.shuffle(self.questions)

        for question in self.questions:
            question.display()

            answer = self.get_user_answer()

            if question.check_answer(answer):
                print("Correct!")
                self.score += 1
            else:
                print("Wrong!")

            print()

        print("Quiz completed!")
        print("Score:", self.score, "/", len(self.questions))

        percentage = (self.score / len(self.questions)) * 100
        print("Percentage:", percentage)



q1 = Question(
    "What is the capital of France?",
    ["A. London", "B. Paris", "C. Rome", "D. Madrid"],
    "B"
)

q2 = Question(
    "Which language are we learning?",
    ["A. Java", "B. C", "C. Python", "D. Swift"],
    "C"
)

q3 = Question(
    "What does OOP stand for?",
    [
        "A. Object Oriented Programming",
        "B. Open Operating Program",
        "C. Object Order Process",
        "D. None"
    ],
    "A"
)

questions = [q1, q2, q3]

quiz = Quiz(questions)

quiz.start()