from typing import TYPE_CHECKING, Optional, TypeVar
import logging

from sk_aio.api import PluginAPI
from sk_aio.models.events import (
    PluginLogEvent,
    ActionProgressEvent,
    ActionErrorEvent,
    ActionCompleteEvent
)

if TYPE_CHECKING:
    from bubus import EventBus

T = TypeVar("T")

class BaseAPI(PluginAPI):
    def __init__(
        self,
        event_bus: 'EventBus',
        plugin_id: str,
    ) -> None:
        self._bus = event_bus
        self._plugin_id = plugin_id
        self._current_action: Optional[str] = None

        # Extra logging data
        self._logger = logging.Logger(self._plugin_id)

    def _create_log_record(
        self,
        message: str,
        level: int = logging.INFO
    ) -> logging.LogRecord:
        filename, line_numer, function_name, _ = self._logger.findCaller(stack_info=False)

        _log_record = logging.LogRecord(
            name=f"{self.plugin_id}.{self.current_action}",
            level=level,
            pathname=filename,
            lineno=line_numer,
            args=(),
            msg=message,
            exc_info=None,
            func=function_name,
            sinfo=None,
        )
        _log_record.__dict__["plugin"] = self.plugin_id
        _log_record.__dict__["action"] = self.current_action

        return _log_record

    def log(
        self,
        message: str,
        level: int = logging.INFO,
    ) -> None:
        self._bus.dispatch(
            PluginLogEvent(
                plugin=self.plugin_id,
                action=self.current_action,
                message=self._create_log_record(message, level),
                level=level
            )
        )

    def debug(self, message: str) -> None:
        return self.log(message, logging.DEBUG)

    def info(self, message: str) -> None:
        return self.log(message, logging.INFO)

    def warning(self, message: str) -> None:
        return self.log(message, logging.WARNING)

    def error(
        self,
        message: str
    ) -> None:
        if self.current_action is None:
            raise ValueError("Error occured when invoking 'ActionErrorEvent' - current_action can't be null.")

        self._bus.dispatch(
            ActionErrorEvent(
                plugin=self.plugin_id,
                action=self.current_action,
                message=self._create_log_record(message, logging.ERROR),
            )
        )

    def progress(
        self,
        percent: float,
    ) -> None:
        if self.current_action is None:
            raise ValueError("Error occured when invoking 'ActionProgressEvent' - current_action can't be null.")

        self._bus.dispatch(
            ActionProgressEvent(
                plugin=self._plugin_id,
                action=self.current_action,
                progresss=percent
            )
        )

    def complete(
        self,
        result: Optional[T] = None,
    ) -> Optional[T]:
        if self.current_action is None:
            raise ValueError("Error occured when invoking 'ActionCompleteEvent' - current_action can't be null.")

        self._bus.dispatch(
            ActionCompleteEvent(
                plugin=self._plugin_id,
                action=self.current_action,
                result=result
            )
        )
        self.current_action = None
        self.log("Task complete!")

    @property
    def current_action(self) -> Optional[str]:
        return self._current_action

    @current_action.setter
    def current_action(self, name: Optional[str]) -> None:
        self._current_action = name

    @property
    def plugin_id(self) -> str:
        return self._plugin_id
