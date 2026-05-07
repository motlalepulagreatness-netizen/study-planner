import json
import os
from StudyPlanner.core.storage_interface import StorageInterface


class Storage(StorageInterface):
    def __init__(self, file_path):
        self._filePath = file_path

    def save(self, student):
        if os.path.exists(self._filePath):
            with open(self._filePath, "w") as f:
                json.dump(student, f, indent=4)
                return True
        else:
            with open(self._filePath, "w") as f:
                json.dump(student, f, indent=4)
                return True
        return True

    def load(self):
        if os.path.exists(self._filePath):
            with open(self._filePath, "r") as f:
                loaded = json.load(f)
            return loaded
        return None
