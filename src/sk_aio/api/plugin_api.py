from typing import Protocol, TypeVar, Optional, TYPE_CHECKING
import logging

T = TypeVar("T")

if TYPE_CHECKING:
    from bubus import EventBus

class PluginAPI(Protocol):
    def __init__(
        event_bus: 'EventBus',
        plugin_id: str
    ) -> None: ...

    def log(
        message: str,
        level: int = logging.INFO
    ) -> None: ...

    def debug(
        self,
        message: str,
    ) -> None: ...

    def info(
        self,
        message: str,
    ) -> None: ...

    def warning(
        self,
        message: str,
    ) -> None: ...

    def error(
        self,
        message: str,
    ) -> None: ...

    def progress(
        percent: float
    ) -> None: ...

    def complete(
        result: Optional[T] = None
    ) -> Optional[T]: ...

    @property
    def current_action(self) -> Optional[str]: ...

    @property
    def plugin_id(self) -> str: ...