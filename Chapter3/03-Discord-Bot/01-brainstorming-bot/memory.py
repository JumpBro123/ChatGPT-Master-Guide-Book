from typing import Dict
from collections import defaultdict


class MemoryInterface:
    def append(self, user_id: str, message: Dict) -> None:
        pass

    def get(self, user_id: str) -> str:
        return ""

    def remove(self, user_id: str) -> None:
        pass


class Memory(MemoryInterface):
    def __init__(self, system_message, memory_message_count):
        self.storage = defaultdict(list)
        self.memory_message_count = memory_message_count
        self.system_message = system_message

    def _initialize(self, user_id: str):
        self.storage[user_id] = [{
            'role': 'system', 'content': self.system_message
        }]

    def _drop_message(self, user_id: str):
        if len(self.storage.get(user_id)) >= (self.memory_message_count + 1) * 2 + 1:
            return [self.storage[user_id][0]] + self.storage[user_id][-(self.memory_message_count * 2):]
        return self.storage.get(user_id)

    def append(self, user_id: str, message: Dict) -> None:
        if self.storage[user_id] == []:
            self._initialize(user_id)
        self.storage[user_id].append(message)
        self._drop_message(user_id)

    def get(self, user_id: str) -> str:
        return self.storage[user_id]

    def remove(self, user_id: str) -> None:
        self.storage[user_id] = []
