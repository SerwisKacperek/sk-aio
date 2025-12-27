from sk_aio.models import BasePlugin

from sk_aio.plugins.file_plugin.actions import ListDirAction, FileExistsAction

class FilePlugin(BasePlugin):
    def __init__(
        self
    ) -> None:
        super().__init__(id="file_plugin", name="File Operations")

        self.register_action(
            ListDirAction(plugin=self)
        )
        self.register_action(
            FileExistsAction(plugin=self)
        )
