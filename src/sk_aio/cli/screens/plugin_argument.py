from typing import TYPE_CHECKING, cast
import logging

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Label
from textual.binding import Binding
from textual.containers import Vertical

from sk_aio.api import PluginAction
from sk_aio.cli.screens import AppHeader
from sk_aio.cli.messages import SwitchToPluginSelectScreen, SwitchToPluginOutputScreen
from sk_aio.cli.widgets import PluginArgumentInput

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne

class PluginArgumentScreen(Screen[None]):
    AUTO_FOCUS = None
    BINDING_GROUP_TITLE = "Plugin Argument Edtior Screen"
    BINDINGS = [
        Binding(
            'ctrl+b',
            'go_screen_back',
            description='Back',
            tooltip='Go back to the Plugin Select screen',
            priority=False,
            id='back-to-plugin-select'
        ),
        Binding(
            'ctrl+r',
            'run_plugin',
            description='Run',
            tooltip='Run the plugin.',
            priority=False,
            id='run-plugin-command'
        )
    ]

    def __init__(
        self,
        action: PluginAction,
    ) -> None:
        super().__init__()

        self.all_in_one_app = cast('AllInOne', self.app)
        self.action: PluginAction = action
        logging.getLogger(__name__).debug([arg.value for arg in action.args])

    def compose(self) -> ComposeResult:
        yield AppHeader()

        with Vertical() as plugin_arguments_area:
            plugin_arguments_area.border_title = "Plugin Arguments"
            plugin_arguments_area.add_class("section")

            yield Label(
                f"[#5457FA]{self.action.plugin.name}:[/]{self.action.name.upper()}\n"
                f"[dim]{self.action.description or ""}[/]",
                id="selected_plugin_name"
            )
            with Vertical() as vertical:
                vertical.border_title = "Plugin arguments"

                groups = dict()
                for arg in self.action.args:
                    groups.setdefault(arg.group, []).append(arg)

                for group_name, args in groups.items():
                    if group_name is not None:
                        yield Label(f"{group_name}")
                    for arg in args:
                        yield Label(f"{arg.name} {"[dim]required[/]" if arg.required else "[dim]optional[/]"}")
                        yield PluginArgumentInput(arg, id=f'{arg.name}-input')

        yield Footer(show_command_palette=False)

    @property
    def can_plugin_run(self) -> bool:
        for arg in self.action.args:
            if arg.required and arg.value is None and arg.default_value is None:
                return False

        return True

# region Actions
    def action_go_screen_back(self) -> None:
        self.app.post_message(SwitchToPluginSelectScreen(self))

    def action_run_plugin(self) -> None:
        """Action which runs the current plugin."""
        if not self.can_plugin_run:
            # TODO: Highlight the required fields
            self.app.notify(
                "Fill in the required fields!", 
                title='Unable to run plugin',
                severity='warning'
            )
            return

        self.app.post_message(
            SwitchToPluginOutputScreen(
                self,
                self.action
            )
        )

# endregion