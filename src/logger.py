# builder.py
import json
import os
from datetime import datetime

DEFAULT_HISTORY_FILE = "build_history.json"

class BuildHistoryManager:
    def __init__(self, file_path=DEFAULT_HISTORY_FILE):
        self.file_path = file_path
        self.builds = []
        self._load_history() 

    def _load_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    self.builds = json.load(f)
                except json.JSONDecodeError:
                    self.builds = []
        else:
            self.builds = []

    def _save_history(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.builds, f, indent=2)

    def add_build(self, commit_id, passed, logs, pusher):
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
        return self.builds

    def get_build_by_id(self, build_id):
        for b in self.builds:
            if b["id"] == build_id:
                return b
        return None
