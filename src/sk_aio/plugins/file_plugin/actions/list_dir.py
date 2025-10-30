import os
from typing import TYPE_CHECKING

from sk_aio.api import PluginAPI, PluginActionArgument
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import FilePlugin

class ListDirAction(BasePluginAction):
    def __init__(self, parent: 'FilePlugin'):
        super().__init__(
            name="list_dir",
            description="Lists files in the given directory",
            method=self.run,
            plugin=parent,
            args=[
            PluginActionArgument(
                name="path",
                required=True,
                type=str,
            ),
            ],
        )

    async def run(self, api: PluginAPI, path: str) -> list[str]:
        api.log(f"Listing directory: {path}")
        result = os.listdir(path)
        api.log(f"Found {len(result)} items.")
        return result
