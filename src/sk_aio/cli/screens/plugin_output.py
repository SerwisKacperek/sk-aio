from typing import TYPE_CHECKING, Any, List, cast

import logging

from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane
from textual.reactive import Reactive, reactive
from textual.containers import Vertical

from sk_aio import logger
from sk_aio.core.logging import BufferedHandler
from sk_aio.models import PluginAction
from sk_aio.cli import SETTINGS
from sk_aio.cli.messages import SwitchToPluginSelectScreen, SwitchToActionArgumentsScreen
from sk_aio.cli.screens import AppHeader
from sk_aio.cli.widgets import TextEditor, ConsoleOutput

from sk_aio.cli.messages import (
    PluginOutputMessage,
    AppUpdateLog,
    ActionProgressMessage,
    ActionCompleteMessage
)

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne
    from sk_aio.core.logging import BufferedHandler

class PluginOutputScreen(Screen[Any]):
    AUTO_FOCUS = None
    BINDING_GROUP_TITLE = "Plugin Output Screen"

    BINDINGS = [
        Binding(
            'ctrl+b',
            'go_screen_back',
            description='Back',
            tooltip='Go back to the Plugin Select screen',
            priority=False,
            id='back-to-plugin-select'
        ),
    ]

    # TODO: Make this app-wide (show also logs from the application and preserve when changing screens)
    console_output: Reactive[List[str]] = reactive([])

    def __init__(
        self,
        action: PluginAction
    ) -> None:
        super().__init__()

        self.all_in_one_app = cast('AllInOne', self.app)
        self.action: PluginAction = action

    async def start_action(self) -> None:
        worker_manager = SETTINGS.get().worker_manager
        worker_manager.run_action(self.action.plugin, self.action)

    def compose(self) -> ComposeResult:
        yield AppHeader()

        # TODO: Create a widget for this area so that it can be accessed from other methods
        with Vertical() as plugin_output_area:
            plugin_output_area.border_title = "Plugin Output"
            plugin_output_area.add_class("section")
            with TabbedContent() as tabbing_content:
                with TabPane("Console"):
                    text_area = ConsoleOutput()
                    yield TextEditor(text_area)
                # TODO: Check if a plugin has any output
                # with TabPane("Output"):
                #     yield

        yield Footer(show_command_palette=False)

    def watch_console_output(
        self,
        console_output: List[str]
    ) -> None:
        if console_output is None:
            return

        console_output_text_area = self.text_editor.text_area
        console_output_text_area.text = "\n".join(console_output)
        console_output_text_area.refresh()

# region Messages
    @on(AppUpdateLog)
    def handle_update_log(self, message: AppUpdateLog) -> None:
        """
        Update the ConsoleOutput widget's content from the BufferHandler.buffer
        """
        handlers: List[BufferedHandler] = list(filter(lambda h: isinstance(h, BufferedHandler), logger.handlers)) # type: ignore
        buffered_handler = next((h for h in handlers if isinstance(h, BufferedHandler)), None)

        # logging.getLogger(__name__).debug("what the helly")
        # logging.getLogger(__name__).debug(buffered_handler)
        # self.app.log("co jest kurwa")
        # self.app.log(buffered_handler)

        if buffered_handler is not None:
            #self.console_output = handlers[0].buffer
            self.console_output = buffered_handler.buffer
            self.watch_console_output(self.console_output)
        else:
            self.app.log("'BufferedHandler' was not found in the 'PluginOutputScreen'!")

    # TODO: REMOVE
    @on(PluginOutputMessage)
    def handle_plugin_output(self, message: PluginOutputMessage) -> None:
        output_string = ""

        output_string += f"[{message.plugin}]"
        if message.action is not None:
            output_string += f"[{message.action}]"
        output_string += f" {message.message}\n"

        self.console_output.append(output_string)
        self.watch_console_output(self.console_output)

    @on(ActionProgressMessage)
    def handle_plugin_progress(self, message: ActionProgressMessage) -> None:
        pass
        #raise NotImplementedError

    @on(ActionCompleteMessage)
    def handle_plugin_complete(self, message: ActionCompleteMessage) -> None:
        pass
        #raise NotImplementedError
# endregion

# region Actions
    def action_go_screen_back(self) -> None:
        if len(self.action.args) == 0:
            self.app.post_message(SwitchToPluginSelectScreen(self))
            return

        self.app.post_message(SwitchToActionArgumentsScreen(self, self.action))
# endregion

# region Properties
    @property
    def text_editor(self) -> TextEditor:
        return self.query_one(TextEditor)
# endregion
