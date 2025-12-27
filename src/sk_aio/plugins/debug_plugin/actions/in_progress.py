from typing import Optional, ClassVar, TYPE_CHECKING

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction, depends_on_action

if TYPE_CHECKING:
    from ..plugin import DebugPlugin
    from sk_aio.plugins.file_plugin.actions import ListDirAction

@depends_on_action('file_plugin', 'list_dir')
class InProgressAction(BasePluginAction):
    name: ClassVar[str] = "in_progress"
    description: ClassVar[Optional[str]] = "Action to debug currently WIP functionality"
    dependencies: dict[str, set[str]] = {}

    def __init__(
        self,
        plugin: 'DebugPlugin',
    ) -> None:
        super().__init__(
            name=InProgressAction.name,
            method=self.run,
            plugin=plugin,
            description=InProgressAction.description,
            args=[]
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

        return
