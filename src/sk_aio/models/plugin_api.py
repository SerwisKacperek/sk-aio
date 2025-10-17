from typing import TYPE_CHECKING, Optional, TypeVar
import logging

from sk_aio.models.events import (
    PluginLogEvent,
    ActionProgressEvent,
    ActionCompleteEvent
)

if TYPE_CHECKING:
    from bubus import EventBus

T = TypeVar("T")

class PluginAPI:

    def __init__(
        self,
        event_bus: 'EventBus',
        plugin_id: str,
    ) -> None:
        self._bus = event_bus
        self._plugin_id = plugin_id
        self._current_action: Optional[str] = None

    def log(
        self,
        message: str,
        level: int = logging.INFO,
    ) -> None:
        self._bus.dispatch(
            PluginLogEvent(
                plugin=self._plugin_id,
                action=self.current_action,
                message=message,
                level=level
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
    def current_action(self, name: Optional[str]):
        self._current_action = name

    @property
    def plugin_id(self):
        return self._plugin_id
