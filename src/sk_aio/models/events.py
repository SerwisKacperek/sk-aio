from typing import Optional, Any
import logging

from bubus import BaseEvent

class AppLogEvent(BaseEvent[None]):
    message: logging.LogRecord
    widget: str
    level: int = logging.INFO

class PluginLogEvent(BaseEvent[None]):
    plugin: str
    action: Optional[str]
    message: logging.LogRecord
    level: int = logging.INFO

class ActionProgressEvent(BaseEvent[None]):
    plugin: str
    action: str
    progresss: float

class ActionErrorEvent(BaseEvent[None]):
    plugin: str
    action: str
    message: logging.LogRecord

class ActionCompleteEvent(BaseEvent[None]):
    plugin: str
    action: str
    result: Optional[Any]
