import random


class Question:
    def __init__(
        self,
        text: str,
        options: list[str],
        correct_answer: str,
    ):
        if not text.strip():
            raise ValueError("Question text cannot be empty.")

        if len(options) < 2:
            raise ValueError(
                "A question must have at least two options."
            )

        correct_answer = correct_answer.strip().upper()

        if correct_answer not in ["A", "B", "C", "D"]:
            raise ValueError(
                "Correct answer must be A, B, C, or D."
            )

        self.text = text.strip()
        self.options = options
        self.correct_answer = correct_answer

    def display(self) -> None:
        print(f"\n{self.text}")

        for option in self.options:
            print(option)

    def check_answer(self, user_answer: str) -> bool:
        return (
            user_answer.strip().upper()
            == self.correct_answer
        )


class Quiz:
    def __init__(self, questions: list[Question]):
        if not questions:
            raise ValueError(
                "Quiz must contain at least one question."
            )

        self.questions = questions
        self.score = 0

    def get_user_answer(self) -> str:
        while True:
            answer = input(
                "Enter your answer (A, B, C, or D): "
            )

            answer = answer.strip().upper()

            if answer in ["A", "B", "C", "D"]:
                return answer

            print(
                "Invalid answer. "
                "Please enter A, B, C, or D."
            )

    def start(self) -> None:
        self.score = 0

        random.shuffle(self.questions)

        print("\n--- Quiz Started ---")

        for question_number, question in enumerate(
            self.questions,
            start=1,
        ):
            print(
                f"\nQuestion {question_number} "
                f"of {len(self.questions)}"
            )

            question.display()

            user_answer = self.get_user_answer()

            if question.check_answer(user_answer):
                print("Correct!")
                self.score += 1

            else:
                print(
                    "Incorrect. "
                    f"The correct answer was "
                    f"{question.correct_answer}."
                )

        self.show_summary()

    def show_summary(self) -> None:
        total_questions = len(self.questions)

        percentage = (
            self.score / total_questions
        ) * 100

        print("\n--- Quiz Summary ---")
        print(f"Score: {self.score}/{total_questions}")
        print(f"Percentage: {percentage:.2f}%")

        if percentage >= 80:
            print("Excellent performance!")

        elif percentage >= 60:
            print("Good job!")

        elif percentage >= 40:
            print("You passed, but keep practising.")

        else:
            print("Keep learning and try again.")


questions = [
    Question(
        "Which keyword is used to define a function in Python?",
        [
            "A. function",
            "B. def",
            "C. create",
            "D. method",
        ],
        "B",
    ),
    Question(
        "Which data structure stores key-value pairs?",
        [
            "A. List",
            "B. Tuple",
            "C. Dictionary",
            "D. Set",
        ],
        "C",
    ),
    Question(
        "What does OOP stand for?",
        [
            "A. Object-Oriented Programming",
            "B. Open Operation Process",
            "C. Object Output Program",
            "D. Ordered Object Processing",
        ],
        "A",
    ),
    Question(
        "Which function is used to get user input?",
        [
            "A. print()",
            "B. read()",
            "C. scan()",
            "D. input()",
        ],
        "D",
    ),
    Question(
        "Which module is used to shuffle a list?",
        [
            "A. math",
            "B. random",
            "C. os",
            "D. json",
        ],
        "B",
    ),
]


if __name__ == "__main__":
    quiz = Quiz(questions)
    quiz.start()