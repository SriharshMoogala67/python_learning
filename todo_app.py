import json 
import os 

tasks = []


def generate_taskid() -> int:
    if not tasks: 
        return 1

    return max(task["id"] for task in tasks) + 1

def add_tasks(title: str) -> None: 

    if not title.strip(): 
        print("title cannot be empty")
        return 
        
    task = {
        "id" : generate_taskid(), 
        "title" : title.strip(),
        "completed" : False 
    }

    tasks.append(task)
    save_tasks()
    print("task saved successfully")

def show_tasks() -> None: 
    if not tasks: 
        print("task list empty")
        return 

    print("\n tasks:")

    for task in tasks: 
        status = "Completed" if task["completed"] else "pending"

        print(
            f'{task["id"]}',
            f'{task["title"]}', 
            f"{status}",
        )

def complete_task(task_id: int) -> bool: 
    for task in tasks: 
        if task["id"] == task_id: 
            if task["completed"] == True: 
                print("task already completed")
                return False

            task["completed"] = True 
            save_tasks() 

            print("task marked as complete")
            return True 

    print("task not found")
    return False 


def delete_tasks(task_id: int) -> bool: 
    for task in tasks: 
        if task["id"] == task_id: 
            tasks.remove(task)
            save_tasks()

            print("task removed successfully")
            return True 

    print("Task not found.")
    return False


def save_tasks(filename: str = "tasks.json") -> None: 
    with open(filename, "w",) as file: 
        json.dump(tasks, file, indent = 4)


def load_tasks(filename: str = "tasks.json") -> None: 
    global tasks 

    if not os.path.exists(filename): 
        tasks = []
        return 

    try: 
        with open(filename, "r") as file: 
            tasks = json.load(file)

    except json.JSONDecodeError: 
        print("the task file is damaged or empty")
        tasks = []



load_tasks()

add_tasks("learn langchain")

show_tasks()

complete_task(4)
complete_task(5)
complete_task(6)