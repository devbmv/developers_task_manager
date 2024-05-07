"""
This module provides functionality for managing tasks for developers. It allows
users to add, modify, delete, and list tasks. Each task includes an ID, date,
time, and description. Tasks are stored in a log file on the user's desktop,
providing easy access and persistent storage.
"""

import os
from time import sleep,strftime,localtime
from pathlib import Path
from colorama import Fore, Back, Style, init

# Initialize an empty list to store tasks
tasks = []

# Initialize task ID based on the current length of tasks
TASK_ID = 1

# Define a separator for visual clarity in the log file
separator = "-" * 200

# Define the filename for storing task logs
file_name = "tasks_log.txt"

# Variable to ensure something is done only once
menu_items = (
    "1: Add task\n"
    "2: Modify task\n"
    "3: Show tasks\n"
    "4: Delete task\n"
    "5: Exit\n"
)

LOG_FILE_NAME = os.getenv("TASKS_LOG_PATH", file_name)

# Determine if the environment is Heroku or similar cloud environment
if "DYNO" in os.environ:
    # We are on Heroku or a similar cloud environment, use a relative path
    full_path = Path(LOG_FILE_NAME)
else:
    # Local environment, attempt to use the desktop for easy access
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / file_name

result_display_time =2
# Ensure the file exists, creating it if necessary
if not full_path.exists():
    # This will create the file in the specified path
    full_path.touch()

# ============================================================================

def input_handler(msg, data_type,min_val=None,max_val=None):
    
    min_val = int(min_val) if min_val is not None else None
    max_val = int(max_val) if max_val is not None else None
    while True:
        
        user_input = input(msg)
        
        if  not user_input:
            print("Input can't be blank, try again:")
            continue
        
        elif min_val is not None and max_val is not None and user_input.isnumeric():
            if (int(user_input)<min_val or int(user_input)>max_val):
                print("Input is not in acceptable range, try again:")
                sleep(result_display_time )
                continue
            
        if data_type == "alfabetic" and user_input.isalpha() or ' ' in user_input:
            return user_input
        elif data_type == "numeric" and user_input.isdigit():
            return user_input
        elif data_type == "alfanumeric" and user_input.isalnum() or ' ' in user_input:
            return user_input
        elif data_type == "float":
            try:
                float(user_input)
                return user_input
            except ValueError:
                pass
        input(Fore.RED + f"\rInput should be {data_type}, press Enter to continue...")


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


def show_tasks():
    clear_screen()
    total_tasks = len(tasks)  # Obține numărul total de task-uri

    for index, task in enumerate(tasks, start=1):
        print(f"{Fore.GREEN}{'-' * 40} Task {index} {'-' * 40}")

        keys = list(task.keys())  # Obține lista de chei din dicționarul task
        last_key = keys[-1]  # Determină ultima cheie

        for data in task:
            if data == last_key:
                # Printează ultima informație cu galben
                print(f"{data}: {Fore.YELLOW}{task[data]}")
            else:
                print(f"{data}: {task[data]}")

        if index == total_tasks:
            # Dacă este ultima iterație, adaugă linia suplimentară
            print(Fore.GREEN+"-" * 88)


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
        count = 1
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
    task_id = (len(tasks) + 1)
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

    Raises:
    - ValueError: If the task_id is not an integer, if it cannot be found in the task list,
                  or if the input is empty.
    """
    global tasks
    try:
        # Validare input gol
        if not task_id:
            raise ValueError("Task ID cannot be empty.")

        # Validare dacă ID-ul task-ului este un număr întreg
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer.")

        # Convert task_id to string (assuming task IDs are stored as strings within the tasks list)
        task_id_str = str(task_id)

        # Verificare dacă task-ul cu ID-ul specificat există în listă
        if not any(task['ID'] == task_id_str for task in tasks):
            raise ValueError(f"No task found with ID {
                             task_id}. Please check the ID and try again.")

        # Filtrare task-uri pentru a elimina task-ul cu ID-ul specificat
        tasks = [task for task in tasks if task["ID"] != task_id_str]
        save_tasks()  # Presupunând că save_tasks() gestionează corect salvarea listei de task-uri actualizată undeva
        print(f"Task ID {task_id} has been successfully deleted.")

    except ValueError as e:
        print(f"Error: {e}")  # Afișarea unui mesaj de eroare specific
    except Exception as e:
        # Capturarea unei excepții generice, care ar putea captura alte erori neașteptate
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
        
        tasks_count=len(tasks)
        
        choice = int(input_handler("Select action between 1 to 5: " + Fore.YELLOW,"numeric",1,5))

        if choice == 1:
            add_task(input(Fore.YELLOW + "Enter task: "))

        elif choice == 2:
            task_id_to_modify = input_handler(
                Fore.YELLOW + "Select id to modify: ",'numeric',0,tasks_count)
            new_description = input_handler(
                Fore.YELLOW + "Enter new description: ","alfanumeric")
            modify_task(task_id_to_modify, new_description)

        elif choice == 3:
            show_tasks()
            input("Press enter to continue...")

        elif choice == 4:
            delete_task(int(input_handler(
                Fore.YELLOW + "Choose task number to delete: ","numeric",1,tasks_count)))
            input("Press enter to continue...")

        elif choice == 5:
            print(Fore.YELLOW + "Good bye !!!")
            sleep(result_display_time )
            break
        sleep(result_display_time )



if __name__ == "__main__":
    main()
