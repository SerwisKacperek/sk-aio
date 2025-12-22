from typing import TYPE_CHECKING

import pyproject_parser as ppp

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction, depends_on_action

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

@depends_on_action('file_plugin', 'list_dir')  # type: ignore[reportArgumentType]
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
        *args,
        **kwargs
    ) -> None:
        path = 'D:\programowanie\SerwisKacperek\sk-aio\src\sk_aio\plugins\debug_plugin\pyproject.toml'
        project = ppp.PyProject.load(path)

        api.info(project.to_dict())
        api.info(self.dependencies)
        api.info(self.plugin._action_deps)

        print(kwargs)

        if "list_dir" in kwargs:
            api.info("list_dir found in kwargs!")
            api.info(kwargs["list_dir"])
            kwargs["list_dir"]()
            api.complete()
        else:
            api.info("list_dir NOT found in kwargs!")

        return
