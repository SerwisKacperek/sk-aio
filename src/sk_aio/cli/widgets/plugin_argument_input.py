from textual import on
from textual.widgets import Input

from sk_aio.models.base_plugin import PluginActionArgument

class PluginArgumentInput(Input):

    def __init__(
        self,
        argument: PluginActionArgument,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._argument = argument

        if argument.value: # TODO: FIX - this should only allow string values here
            self.value = str(argument.value)

    # region Messages
    @on(Input.Changed)
    def handle_input_changed(self, event: Input.Changed) -> None:
        # TODO: Validate first
        self._argument.value = event.value

# endregion
