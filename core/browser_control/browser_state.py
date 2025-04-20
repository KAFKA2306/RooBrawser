from enum import Enum

class BrowserState(Enum):
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    RESPONSE_PENDING = "RESPONSE_PENDING"
    RESPONSE_READY = "RESPONSE_READY"
    ERROR = "ERROR"
    CLOSED = "CLOSED"