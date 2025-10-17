from sk_aio.models import BasePlugin

from sk_aio.plugins.debug_plugin.actions import (
    ConsoleOutputAction,
    AsyncAction,
    MultipleArgumentsActions
)

class DebugPlugin(BasePlugin):
    def __init__(
        self
    ) -> None:
        super().__init__(id="debug_plugin", name="Debug Plugin")

        self.register_action(
            ConsoleOutputAction(parent=self)
        )
        self.register_action(
            MultipleArgumentsActions(parent=self)
        )
        self.register_action(
            AsyncAction(parent=self)
        )
