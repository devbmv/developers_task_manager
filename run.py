"""
This module provides functionality for managing tasks for developers. It allows
users to add, modify, delete, and list tasks. Each task includes an ID, date,
time, and description. Tasks are stored in a log file on the user's desktop,
providing easy access and persistent storage.
"""

import os
from time import sleep, strftime, localtime
from pathlib import Path
from colorama import Fore, init

# Initialize an empty list to store tasks
tasks = []

# Initialize task ID based on the current length of tasks
TASK_ID = 0

# Define a separator for visual clarity in the log file
separator = "-" * 200

# Define the filename for storing task logs
file_name = "tasks_log.txt"

# Menu items for display
menu_items = (
    "1: Add task\n"
    "2: Modify task\n"
    "3: Show tasks\n"
    "4: Delete task\n"
    "5: Exit\n"
)

# Get log file name from environment variable or default to file_name
LOG_FILE_NAME = os.getenv("TASKS_LOG_PATH", file_name)

# Determine if the environment is Heroku or similar cloud environment
if "DYNO" in os.environ:
    # We are on Heroku or a similar cloud environment, use a relative path
    full_path = Path(LOG_FILE_NAME)
else:
    # Local environment, attempt to use the desktop for easy access
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / file_name

result_display_time = 2

# Ensure the file exists, creating it if necessary
if not full_path.exists():
    # This will create the file in the specified path
    full_path.touch()

# ============================================================================


def input_handler(msg, data_type, min_val=None, max_val=None):
    """
    Handles and validates user input based on the specified data type
    and optional min and max values.

    Parameters:
    - msg (str): The message to display to the user.
    - data_type (str): The type of data expected ('alfabetic', 'numeric',
     'alfanumeric', 'float').
    - min_val (int, optional): The minimum acceptable value.
    - max_val (int, optional): The maximum acceptable value.

    Returns:
    - user_input: The validated user input.
    """
    min_val = int(min_val) if min_val is not None else None
    max_val = int(max_val) if max_val is not None else None
    while True:
        user_input = input(msg)

        if not user_input:
            print("Input can't be blank, try again:")
            continue

        if (min_val is not None and max_val
                is not None and user_input.isnumeric()):
            if int(user_input) < min_val or int(user_input) > max_val:
                print("Input is not in acceptable range, try again:")
                sleep(result_display_time)
                continue

        if (data_type == "alfabetic" and
                user_input.isalpha() or ' ' in user_input):
            return user_input
        elif data_type == "numeric" and user_input.isdigit():
            return user_input
        elif (data_type == "alfanumeric" and
              user_input.isalnum() or ' ' in user_input):
            return user_input
        elif data_type == "float":
            try:
                float(user_input)
                return user_input
            except ValueError:
                pass
        input(
            Fore.RED + f"\rInput should be {data_type},"
            "press Enter to continue...")


# ============================================================================


def clear_screen():
    """
    Clears the console screen based on the operating system.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# ============================================================================


def show_tasks():
    """
    Displays all tasks stored in the global tasks list.
    """
    clear_screen()
    total_tasks = len(tasks)

    for index, task in enumerate(tasks, start=0):
        print(f"{Fore.GREEN}{'-' * 40} Task {index} {'-' * 40}")

        keys = list(task.keys())
        last_key = keys[-1]

        for data in task:
            if data == last_key:
                print(f"{data}: {Fore.YELLOW}{task[data]}")
            else:
                print(f"{data}: {task[data]}")

        if index == total_tasks:
            print(Fore.GREEN + "-" * 88)


# ============================================================================


def load_tasks():
    """
    Loads tasks from the log file into the global tasks list.
    """
    global tasks
    tasks.clear()
    with open(full_path, "r", encoding="utf-8") as file:
        task_data = file.read().strip().split("-" * 74 + "\n")[1:]
        for task_block in task_data:
            task_info = task_block.strip().split("\n")
            task_dict = {}
            for line in task_info:
                if ":" in line:
                    key, value = line.split(":", 1)
                    task_dict[key.strip()] = value.strip()
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
    Adds a new task with the given description to the tasks list
    and logs it to the file.

    Parameters:
    - description (str): The description of the task to be added.
    """
    task_id = len(tasks) + 1
    now = localtime()
    task = {
        "ID": str(task_id),
        "Date": strftime("%Y-%m-%d", now),
        "Time": strftime("%H:%M:%S", now),
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
    try:
        if task_id is None or task_id == "":
            raise ValueError("Task ID cannot be empty.")

        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer.")

        task_id_str = str(task_id)

        task_to_delete = None
        for task in tasks:
            if task['ID'] == task_id_str:
                task_to_delete = task
                break

        if task_to_delete:
            tasks.remove(task_to_delete)
            save_tasks()
            print(f"Task ID {task_id} has been successfully deleted.")
        else:
            raise ValueError(
                f"No task found with ID {task_id}"
                ". Please check the ID and try again.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press enter to continue...")


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
        if task["ID"] == str(task_id):
            task["Task"] = new_description
            found = True
            break

    if found:
        save_tasks()
        print(
            f"Task ID {task_id} has been"
            "successfully modified to: '{new_description}'.")
    else:
        print(f"Task ID {task_id} not found.")


# ============================================================================


def main():
    """
    The main function of the program. Handles user interaction.
    """
    init()
    load_tasks()

    while True:
        clear_screen()
        print(Fore.GREEN + "Developers Task Manager:\n")
        print(menu_items)

        tasks_count = len(tasks)

        choice = int(input_handler(
            "Select action between 1 to 5: " + Fore.YELLOW, "numeric", 1, 5))

        if choice == 1:
            add_task(input_handler(Fore.YELLOW +
                                   "Enter task: ", "alfanumeric"))

        elif choice == 2:
            task_id_to_modify = input_handler(
                Fore.YELLOW + "Select id to modify: ",
                'numeric', 0, tasks_count)
            new_description = input_handler(
                Fore.YELLOW + "Enter new description: ", "alfanumeric")
            modify_task(task_id_to_modify, new_description)

        elif choice == 3:
            show_tasks()
            input("Press enter to continue...")

        elif choice == 4:
            delete_task(int(input_handler(
                Fore.YELLOW + "Choose task number to delete: ",
                "numeric", 0, tasks_count)))
            input("Press enter to continue...")

        elif choice == 5:
            print(Fore.YELLOW + "Good bye !!!")
            sleep(result_display_time)
            break
        sleep(result_display_time)


if __name__ == "__main__":
    main()
