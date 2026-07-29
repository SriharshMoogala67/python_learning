students = []

def add_students(name: str, marks: int) -> None:  
    student = {

        "name": name, 
        "marks": marks, 
        "passed": marks >= 40,
    }

    students.append(student)


def show_students() -> None: 
    for index, student in enumerate(students, start = 1):
        status = "Passed" if student["passed"] else "failed"

        print(
            index, 
            student["name"], 
            student["marks"], 
            status, 
        )

def find_topstudent() -> dict | None:
    if not students: 
        return None

    topstud = students[0]
    for stud in students: 

        if stud["marks"] > topstud["marks"]:
            topstud = stud

    return topstud

add_students("harsh", 100)
add_students("rahul", 50)
add_students("aman", 20)


top = find_topstudent()
print(top["name"])

def avg() -> int: 
    total = 0

    for student in students:
        total += student["marks"]

    average = total / len(students)

    return average

ave = avg()
print(ave)