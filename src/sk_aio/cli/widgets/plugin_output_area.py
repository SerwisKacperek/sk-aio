from typing import Literal, Any

from textual.containers import Vertical
from textual.reactive import Reactive, reactive

class PluginOutputArea(Vertical):
    plugin_action_state: Reactive[Literal[-1, 0 , 1]] = reactive(0)
    """
    plugin_action_state:
        -1 Error occured during action's execution
        0 Action still running
        1 Action completed succesfully
    """
    plugin_action_result: Reactive[Any | None] = reactive(None)

    def __init__(self) -> None:
        super().__init__()

        self.border_title = "Plugin Output"
        self.add_class("section")

    def watch_plugin_action_state(self) -> None:
        """When this value get's changed, update the widget's style"""
        self.remove_class("action_complete")
        self.remove_class("action_error")

        match self.plugin_action_state:
            case -1:
                self.add_class("action_error")
            case 1:
                self.add_class("action_complete")

        return
