from abc import ABC, abstractmethod


class StorageInterface(ABC):
    def save(self, student):
        pass

    def load(self):
        pass
