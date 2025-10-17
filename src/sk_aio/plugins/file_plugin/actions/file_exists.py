import os
from typing import TYPE_CHECKING

from sk_aio.models import PluginAction, PluginActionArgument, PluginAPI

if TYPE_CHECKING:
    from ..plugin import FilePlugin

class FileExistsAction(PluginAction):
    def __init__(self, parent: 'FilePlugin'):
        super().__init__(
            name="check_file",
            description="Checks if a file with a given directory exists",
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

    async def run(self, api: PluginAPI, path: str) -> bool:
        api.log(f"Checking if file exists: {path}")
        exists = os.path.isfile(path)
        api.log(f"File exists: {exists}")
        return exists
