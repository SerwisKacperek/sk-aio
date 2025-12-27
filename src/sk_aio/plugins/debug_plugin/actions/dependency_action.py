from typing import Optional, TYPE_CHECKING

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction, depends_on_action

if TYPE_CHECKING:
    from ..plugin import DebugPlugin
    from sk_aio.plugins.file_plugin.actions import ListDirAction

@depends_on_action('file_plugin', 'list_dir')
class DependencyAction(BasePluginAction):
    def __init__(self, plugin: 'DebugPlugin') -> None:
        super().__init__(
            name="dependency_action",
            description="This action ensures if the action dependencies checks are working correctly",
            method=self.run,
            plugin=plugin,
            args=None
        )

    async def run(
        self,
        api: PluginAPI,
        *args,
        list_dir: Optional['ListDirAction'] = None,
        **kwargs
    ) -> None:

        if list_dir is None:
            api.info("list_dir argument is None!")
            return

        api.info("list_dir argument present!")
        result = await list_dir.run(api, "D:/")
        api.log(str(result))
        api.log("Done")

