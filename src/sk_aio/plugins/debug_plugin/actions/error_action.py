from typing import TYPE_CHECKING

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class ErrorAction(BasePluginAction):
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
