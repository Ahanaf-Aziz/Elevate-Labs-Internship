import os
TASKS_FILE = 'tasks.txt'
def load_tasks():
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = [line.strip() for line in file]
    return tasks
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        for task in tasks:
            file.write(task + '\n')
def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.\n")
    else:
        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")
        print()
def add_task(tasks):
    task = input("Enter new task: ").strip()
    if task:
        tasks.append(task)
        print(f"Task added: {task}\n")
    else:
        print("Task cannot be empty.\n")
def remove_task(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            idx = int(input("Enter the task number to remove: "))
            if 1 <= idx <= len(tasks):
                removed = tasks.pop(idx - 1)
                print(f"Task removed: {removed}\n")
            else:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.\n")
def main():
    tasks = load_tasks()
    while True:
        print("To-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
            save_tasks(tasks)
        elif choice == '3':
            remove_task(tasks)
            save_tasks(tasks)
        elif choice == '4':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.\n")
if __name__ == '__main__':
    main()
