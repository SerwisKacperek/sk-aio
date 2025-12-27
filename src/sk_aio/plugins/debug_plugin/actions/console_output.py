from typing import TYPE_CHECKING
import logging

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class ConsoleOutputAction(BasePluginAction):
    def __init__(self, plugin: 'DebugPlugin') -> None:
        super().__init__(
            name="console_output",
            description="Outputs a single string into the console",
            method=self.run,
            plugin=plugin,
            args=None
        )

    async def run(self, api: PluginAPI) -> None:
        api.log("Hello World!", level=logging.INFO)
        return
