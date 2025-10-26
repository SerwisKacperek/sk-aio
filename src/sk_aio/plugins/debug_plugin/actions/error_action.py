from typing import TYPE_CHECKING

from sk_aio.models import PluginAction, PluginAPI

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class ErrorAction(PluginAction):
    def __init__(self, parent: 'DebugPlugin') -> None:
        super().__init__(
            name="error_action",
            description="Triggers an error during the action's runtime",
            method=self.run,
            plugin=parent,
            args=None
        )

    async def run(self, api: PluginAPI) -> None:
        raise RuntimeError("This is a test exception for debugging purposes.")
