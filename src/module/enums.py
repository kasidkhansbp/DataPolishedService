from enum import Enum

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class V(int):
    REPAIR_BACKOFF = 1.5  # seconds
    MAX_RETRIES = 3