import sys
from typing import TYPE_CHECKING

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class DependencyAction(BasePluginAction):
    def __init__(self, parent: 'DebugPlugin') -> None:
        super().__init__(
            name="dependency_action",
            description="This action ensures if the action dependencies checks are working correctly",
            method=self.run,
            plugin=parent,
            args=None
        )

    async def run(self, api: PluginAPI) -> None:

        for name in sys.modules:
            if "sk_aio.plugins." in name:
                api.info(name)
        api.info("Hello World!")
        return
