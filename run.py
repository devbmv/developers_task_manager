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

LOG_FILE_NAME = os.getenv("TASKS_LOG_PATH", "tasks_log.txt")

# Check if the LOG_FILE_NAME is an absolute path, if not, use the desktop path
if os.path.isabs(LOG_FILE_NAME):
    full_path = LOG_FILE_NAME
else:
    # If running locally, store the tasks log on the desktop for easy access
    desktop_path = Path.home() / "Desktop"
    full_path = desktop_path / file_name


def main():
    """
    The main function of the program. Handles user interaction.
    """


if __name__ == "__main__":
    main()
