from typing import TYPE_CHECKING, Optional, Any
from textual.message import Message
import logging

if TYPE_CHECKING:
    from sk_aio.cli.screens import (
        PluginSelectScreen,
        PluginArgumentScreen,
        PluginOutputScreen,
    )
    from sk_aio.models import PluginAction
    from sk_aio.cli.events import AppLogEvent, PluginLogEvent

class SwitchToPluginSelectScreen(Message):
    """Notify the main app to switch to the plugin select screen."""

    def __init__(
        self,
        screen: 'PluginArgumentScreen | PluginOutputScreen'
    ) -> None:
        self.screen = screen
        super().__init__()

    @property
    def control(self) -> 'PluginArgumentScreen | PluginOutputScreen':
        return self.screen

class SwitchToActionArgumentsScreen(Message):
    """Notify the main app to switch to the action argument editor screen."""

    ALLOW_SELECTOR_MATCH = { "action "}

    def __init__(
        self,
        screen: 'PluginSelectScreen | PluginOutputScreen',
        action: 'PluginAction'
    ) -> None:
        self.screen = screen
        self.action = action
        super().__init__()

    @property
    def control(self) -> 'PluginSelectScreen | PluginOutputScreen':
        return self.screen

class SwitchToPluginOutputScreen(Message):
    """Notify the main app to switch to the plugin output screen."""

    ALLOW_SELECTOR_MATCH = { "action" }

    def __init__(
        self,
        screen: 'PluginSelectScreen | PluginArgumentScreen',
        action: 'PluginAction'
    ) -> None:
        self.screen = screen
        self.action = action
        super().__init__()

    @property
    def control(
        self
    ) -> 'PluginSelectScreen | PluginArgumentScreen':
        return self.screen

class AppUpdateLog(Message):
    def __init__(
        self,
        event: "AppLogEvent | PluginLogEvent",
    ) -> None:
        self.event = event
        super().__init__()

class ActionProgressMessage(Message):
    def __init__(
        self,
        plugin: str,
        action: str,
        progresss: float
    ) -> None:
        self.plugin = plugin
        self.action = action
        self.progress = progresss
        super().__init__()

class ActionCompleteMessage(Message):
    def __init__(
        self,
        plugin: str,
        action: str,
        result: Optional[Any]
    ) -> None:
        self.plugin = plugin
        self.action = action
        self.result = result
        super().__init__()
