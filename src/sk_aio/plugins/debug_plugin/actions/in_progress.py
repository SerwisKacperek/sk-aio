from typing import TYPE_CHECKING

import pyproject_parser as ppp

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class InProgressAction(BasePluginAction):
    def __init__(
        self,
        parent: 'DebugPlugin'
    ) -> None:
        super().__init__(
            name="in_progress",
            description="Action to debug currently WIP functionality",
            method=self.run,
            plugin=parent,
            args=None
        )

    async def run(
        self,
        api: PluginAPI,
    ) -> None:
        path = 'D:\programowanie\SerwisKacperek\sk-aio\src\sk_aio\plugins\debug_plugin\pyproject.toml'
        project = ppp.PyProject.load(path)
        api.info(project.to_dict())

        return