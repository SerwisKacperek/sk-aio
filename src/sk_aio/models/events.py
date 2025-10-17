from typing import Optional, Any
import logging

from bubus import BaseEvent

class AppLogEvent(BaseEvent[None]):
    message: str
    widget: str
    level: int = logging.INFO

class PluginLogEvent(BaseEvent[None]):
    plugin: str
    action: Optional[str]
    message: str
    level: int = logging.INFO

class ActionProgressEvent(BaseEvent[None]):
    plugin: str
    action: str
    progresss: float

class ActionCompleteEvent(BaseEvent[None]):
    plugin: str
    action: str
    result: Optional[Any]
