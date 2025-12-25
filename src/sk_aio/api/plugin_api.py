from typing import Protocol, TypeVar, Optional, TYPE_CHECKING
import logging

T = TypeVar("T")

if TYPE_CHECKING:
    from bubus import EventBus
    from sk_aio.api import PluginAction
    from sk_aio.core import AppContext

class PluginAPI(Protocol):
    _context: 'AppContext'
    _bus: 'EventBus'
    _plugin_id: str
    _current_action: Optional[str] = None

    def __init__(
        self,
        context: 'AppContext',
        plugin_id: str
    ) -> None: ...

    @property
    def current_action(self) -> Optional[str]: ...

    @property
    def plugin_id(self) -> str: ...

    def execute(self, action: 'PluginAction'): ...

    def log(
        self,
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
        self,
        percent: float
    ) -> None: ...

    def complete(
        self,
        result: Optional[T] = None
    ) -> Optional[T]: ...
