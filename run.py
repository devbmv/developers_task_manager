"""
This module provides functionality for managing tasks for developers. It allows
users to add, modify, delete, and list tasks. Each task includes an ID, date,
time, and description. Tasks are stored in a log file on the user's desktop,
providing easy access and persistent storage.
"""

import os
import time
from pathlib import Path
from colorama import init, Fore

# Initialize an empty list to store tasks
tasks = []
# Initialize task ID based on the current length of tasks
TASK_ID = 0
# Define a separator for visual clarity in the log file
separator = "-" * 200
# Define the filename for storing task logs
file_name = "tasks_log.txt"

LOG_FILE_NAME = os.getenv("TASKS_LOG_PATH", file_name)

# Determine if the environment is Heroku or similar cloud environment
if "DYNO" in os.environ:
    # We are on Heroku or a similar cloud environment, use a relative path
    full_path = Path(LOG_FILE_NAME)
else:
    # Local environment, attempt to use the desktop for easy access
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / file_name

# Ensure the file exists, creating it if necessary
if not full_path.exists():
    # This will create the file in the specified path
    full_path.touch()

# ============================================================================

menu_items = (
    "1: Add task\n"
    "2: Modify task\n"
    "3: Show tasks\n"
    "4: Delete task\n"
    "5: Exit\n"
)

# ============================================================================


def load_tasks():
    """
    Loads tasks from the log file into the global tasks list.
    """
    global tasks
    tasks.clear()
    with open(full_path, "r", encoding="utf-8") as file:
        # Skip the header by splitting on the task separator
        task_data = file.read().strip().split("-" * 74 + "\n")[1:]
        for task_block in task_data:
            task_info = task_block.strip().split("\n")
            task_dict = {}
            for line in task_info:
                if ":" in line:  # Check if the line contains a colon
                    key, value = line.split(":", 1)
                    task_dict[key.strip()] = value.strip()
                else:
                    # Handle lines without a colon.
                    pass
            tasks.append(task_dict)


# ============================================================================


def save_tasks():
    """
    Saves tasks from the global tasks list to the log file.
    """
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(f"{'-'*92} List Of Tasks: {'-'*92}\n")
        count = 0
        for task in tasks:
            task["ID"] = str(count)
            for key, value in task.items():
                file.write(f"{key}: {value}\n")
            count += 1
            file.write(f"{separator}\n")


# ============================================================================


def add_task(description):
    """
    Adds a new task with the given description to the
    tasks list and logs it to the file.
    Parameters:
    - description (str): The description of the task to be added.
    """
    task_id = len(tasks) + 1
    now = time.localtime()
    task = {
        "ID": str(task_id),
        "Date": time.strftime("%Y-%m-%d", now),
        "Time": time.strftime("%H:%M:%S", now),
        "Task": description,
    }
    tasks.append(task)
    save_tasks()
    print(f"Task ID {task_id}: '{description}' successfully added.")


# ============================================================================


def delete_task(task_id):
    """
    Deletes a task based on its ID.

    Parameters:
    - task_id (int): The ID of the task to be deleted.
    """
    global tasks
    task_id = str(task_id)
    tasks = [task for task in tasks if task["ID"] != task_id]
    save_tasks()
    print(f"Task ID {task_id} has been successfully deleted.")


# ============================================================================


def modify_task(task_id, new_description):
    """
    Modifies the description of a task based on its ID.

    Parameters:
    - task_id (int): The ID of the task to modify.
    - new_description (str): The new description for the task.
    """
    found = False
    for task in tasks:
        if task["ID"] == task_id:
            task["Task"] = new_description
            found = True
            break
    if found:
        save_tasks()
        print(
            f"Task ID {task_id} has been successfully modified to:"
            + f"'{new_description}'."
        )

    else:
        print(f"Task ID {task_id} not found.")


# ============================================================================


def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    # Check if the operating system is Windows
    if os.name == "nt":
        os.system("cls")
    else:
        # Assume the operating system is Unix/Linux/Mac
        os.system("clear")


# ============================================================================


def main():
    """
    The main function of the program. Handles user interaction.
    """

    init()

    load_tasks()
    print(Fore.GREEN + "Welcome to Developers' Task Manager")

    while True:

        time.sleep(1)
        clear_screen()

        print("Developers Task Manager:\n")
        print(menu_items)
        choice = input("Select action: ")

        try:
            if choice == "1":

                add_task(input("Enter task: "))

            elif choice == "2":

                task_id_to_modify = input("Select id to modify: ")
                new_description = input("Enter new description: ")
                modify_task(task_id_to_modify, new_description)

            elif choice == "3":

                delete_task(int(input("Choice task number: ")))

            elif choice == "4":

                break

            else:

                print("Invalid selection. Please try again.")

        except Exception as e:

            print(f"An error occurred: {e}")


# ============================================================================

if __name__ == "__main__":
    main()

# ============================================================================
