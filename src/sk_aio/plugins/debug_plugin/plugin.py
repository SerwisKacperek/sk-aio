from typing import ClassVar

from sk_aio.models import BasePlugin

from sk_aio.plugins.debug_plugin.actions import (
    ConsoleOutputAction,
    AsyncAction,
    MultipleArgumentsActions,
    ErrorAction,
    DependencyAction,
    InProgressAction
)

class DebugPlugin(BasePlugin):
    id: ClassVar[str] = "debug_plugin"
    name: ClassVar[str] = "Debug Plugin"

    def __init__(
        self
    ) -> None:
        super().__init__(
            id=DebugPlugin.id,
            name=DebugPlugin.name
        )

        self.register_action(
            ConsoleOutputAction(plugin=self)
        )
        self.register_action(
            MultipleArgumentsActions(plugin=self)
        )
        self.register_action(
            AsyncAction(plugin=self)
        )
        self.register_action(
            ErrorAction(plugin=self)
        )
        self.register_action(
            DependencyAction(plugin=self)
        )
        self.register_action(
            InProgressAction(plugin=self)
        )
