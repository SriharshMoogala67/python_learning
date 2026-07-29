import json
import os


tasks = []


def generate_task_id() -> int:
    """Generate a unique ID for a new task."""
    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def save_tasks(filename: str = "tasks.json") -> None:
    """Save all tasks to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def load_tasks(filename: str = "tasks.json") -> None:
    """Load saved tasks from a JSON file."""
    global tasks

    if not os.path.exists(filename):
        tasks = []
        return

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)

    except json.JSONDecodeError:
        print("The tasks file is empty or damaged.")
        tasks = []

    except OSError as error:
        print(f"Could not load tasks: {error}")
        tasks = []


def add_task(title: str) -> bool:
    """Add a new task."""
    clean_title = title.strip()

    if not clean_title:
        print("Task title cannot be empty.")
        return False

    task = {
        "id": generate_task_id(),
        "title": clean_title,
        "completed": False,
    }

    tasks.append(task)
    save_tasks()

    print("Task added successfully.")
    return True


def show_tasks() -> None:
    """Display all tasks."""
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Your Tasks ---")

    for task in tasks:
        status = "Complete" if task["completed"] else "Pending"

        print(
            f'{task["id"]}. '
            f'{task["title"]} - '
            f'{status}'
        )


def complete_task(task_id: int) -> bool:
    """Mark a task as complete."""
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print("Task is already complete.")
                return False

            task["completed"] = True
            save_tasks()

            print("Task marked as complete.")
            return True

    print("Task not found.")
    return False


def delete_task(task_id: int) -> bool:
    """Delete a task."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks()

            print("Task deleted successfully.")
            return True

    print("Task not found.")
    return False


def show_menu() -> None:
    """Display the application menu."""
    print("\n--- To-Do List ---")
    print("1. Show tasks")
    print("2. Add task")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Exit")


def main() -> None:
    """Run the to-do list application."""
    load_tasks()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_tasks()

        elif choice == "2":
            title = input("Enter task title: ")
            add_task(title)

        elif choice == "3":
            try:
                task_id = int(
                    input("Enter task ID to complete: ")
                )
                complete_task(task_id)

            except ValueError:
                print("Please enter a valid numeric task ID.")

        elif choice == "4":
            try:
                task_id = int(
                    input("Enter task ID to delete: ")
                )
                delete_task(task_id)

            except ValueError:
                print("Please enter a valid numeric task ID.")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()