from typing import Optional, TYPE_CHECKING

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction, depends_on_action

if TYPE_CHECKING:
    from ..plugin import DebugPlugin
    from sk_aio.plugins.file_plugin.actions import ListDirAction

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
        list_dir: Optional['ListDirAction'] = None,
        *args,
        **kwargs
    ) -> None:

        if list_dir is None:
            api.info("list_dir argument is None!")
            return

        api.info("list_dir argument present!")
        result = await list_dir.run(api, "D:/")
        api.log("Done")

        return
