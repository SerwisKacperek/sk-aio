from typing import TYPE_CHECKING, Any, List, cast

import logging

from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane, Log
from textual.reactive import Reactive, reactive

from sk_aio import logger
from sk_aio.core.logging import BufferedHandler, CustomTextLogFormatter
from sk_aio.api import PluginAction
from sk_aio.cli.messages import SwitchToPluginSelectScreen, SwitchToActionArgumentsScreen
from sk_aio.cli.screens import AppHeader
from sk_aio.cli.widgets import PluginOutputArea

from sk_aio.cli.messages import (
    AppUpdateLog,
    ActionProgressMessage,
    ActionErrorMessage,
    ActionCompleteMessage
)

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne

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

    console_output: Reactive[List[str]] = reactive([])

    def __init__(
        self,
        action: PluginAction
    ) -> None:
        super().__init__()

        self.all_in_one_app = cast('AllInOne', self.app)
        self.action: PluginAction = action

    async def start_action(self) -> None:
        self.all_in_one_app.context.worker_manager.run_action(self.action.plugin, self.action)

    def on_mount(self) -> None:
        handlers: List[BufferedHandler] = list(filter(lambda h: isinstance(h, BufferedHandler), logger.handlers)) # type: ignore
        buffered_handler = next((h for h in handlers if isinstance(h, BufferedHandler)), None)

        if buffered_handler is not None:
            self.console_output = self._format_log_records(buffered_handler.buffer)
        else:
            self.app.log("'BufferedHandler' was not found in the 'PluginOutputScreen'!")

    def compose(self) -> ComposeResult:
        yield AppHeader()

        with PluginOutputArea():
            with TabbedContent():
                with TabPane("Console"):
                    yield Log(auto_scroll=True)
                # TODO: Check if a plugin has any output
                # with TabPane("Output"):
                #     yield

        yield Footer(show_command_palette=False)

    def watch_console_output(self) -> None:
        """Update the 'Log' widget, whenever the console_output value changes"""
        if self.console_output is None:
            return

        self.log_widget.clear()
        self.log_widget.write_lines(self.console_output)

    @staticmethod
    def _format_log_records(records: List[logging.LogRecord]) -> List[str]:
        _formatter = CustomTextLogFormatter()

        return [ _formatter.format(msg) for msg in records ]

# region Messages
    @on(AppUpdateLog)
    def handle_update_log(self, message: AppUpdateLog) -> None:
        """
        Update the ConsoleOutput widget's content from the BufferHandler.buffer
        """
        handlers: List[BufferedHandler] = list(filter(lambda h: isinstance(h, BufferedHandler), logger.handlers)) # type: ignore
        buffered_handler = next((h for h in handlers if isinstance(h, BufferedHandler)), None)

        if buffered_handler is not None:
            self.console_output = self._format_log_records(buffered_handler.buffer)
        else:
            self.app.log("'BufferedHandler' was not found in the 'PluginOutputScreen'!")

    @on(ActionProgressMessage)
    def handle_action_progress(self, message: ActionProgressMessage) -> None:
        pass

    @on(ActionErrorMessage)
    def handle_action_error(self, message: ActionErrorMessage) -> None:
        self.plugin_output_area_widget.plugin_action_state = -1

    @on(ActionCompleteMessage)
    def handle_action_complete(self, message: ActionCompleteMessage) -> None:
        logging.getLogger(__name__).debug("%s.%s action complete!", message.plugin, message.action)
        self.plugin_output_area_widget.plugin_action_state = 1

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
    def log_widget(self) -> Log:
        return self.query_one(Log)

    @property
    def plugin_output_area_widget(self) -> PluginOutputArea:
        return self.query_one(PluginOutputArea)
# endregion
