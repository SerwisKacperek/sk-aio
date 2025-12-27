from typing import Any, TYPE_CHECKING

from sk_aio.api import PluginAPI, PluginActionArgument
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class MultipleArgumentsActions(BasePluginAction):
    def __init__(self, plugin: 'DebugPlugin') -> None:
        super().__init__(
            name="multiple_arguments",
            description="Requires multiple arguments to be passed to run the action.",
            method=self.run,
            plugin=plugin,
            args=[
                PluginActionArgument(
                    name="arg1",
                    required=False,
                    type=str
                ),
                PluginActionArgument(
                    name="arg2",
                    required=False,
                    type=type[Any],
                    group="Arguments #2"
                )
            ]
        )

    async def run(self, api: PluginAPI, *args, **kwargs) -> None:

        for i, arg in enumerate(args):
            api.log(f"arg[{i}]: {arg}")

        for key, value in kwargs.items():
            api.log(f"arg[{key}]: {value}")

        api.log("Done")

        return
