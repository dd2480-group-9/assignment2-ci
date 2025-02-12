"""
logger.py

This module provides a class,BuildHistoryManager , that includes functionalities
that can load past builds and save new ones

"""
import json
import os
from datetime import datetime

DEFAULT_HISTORY_FILE = "build_history.json"

class BuildHistoryManager:
    """
    Handles logging.

    Attributes:
        file_path (str): The path to the JSON file.
        builds (list[dict]): Contains 'id', 'commit_id', 'pusher', 'status',
                             'timestamp', and 'logs'.
    """
    def __init__(self, file_path=DEFAULT_HISTORY_FILE):
        """
        Initializes the class by loading preexisting logs.

        Args:
            file_path (str, optional): The path to the JSON file.
        """
        self.file_path = file_path
        self.builds = []
        self._load_history() 

    def _load_history(self):
        """
        Initializes an empty list if there is no file. If there is,
        builds the existing logs.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    self.builds = json.load(f)
                except json.JSONDecodeError:
                    self.builds = []
        else:
            self.builds = []

    def _save_history(self):
        """
        Loads the current build histoy to json file in file_path.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.builds, f, indent=2)

    def add_build(self, commit_id, passed, logs, pusher):
        """
        Adds a new build record to the list of builds.

        Args:
            commit_id (str): The SHA.
            passed (bool): Whether the build or tests passed successfully.
            logs (str): Output logs from the tests.
            pusher (str): Username of who pushed the commit.

        Returns:
            int: The unique build ID assigned to the new log.
        """
        build_id = len(self.builds) + 1
        new_build = {
            "id": build_id,
            "commit_id": commit_id,
            "pusher": pusher or "unknown", 
            "status": "success" if passed else "failed",
            "timestamp": datetime.utcnow().isoformat(),
            "logs": logs
        }
        self.builds.append(new_build)
        self._save_history()
        return build_id

    def get_all_builds(self):
        """
        Retrieves all recorded builds.

        Returns:
            list[dict]: List of all build records.
        """
        return self.builds

    def get_build_by_id(self, build_id):
        """
        Finds and returns a build log by its build ID.

        Args:
            build_id (int): The unique build ID.

        Returns:
            dict | None: The build record if found, otherwise None.
        """
        for b in self.builds:
            if b["id"] == build_id:
                return b
        return None
