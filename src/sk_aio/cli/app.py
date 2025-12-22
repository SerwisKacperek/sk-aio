from typing import Optional, TYPE_CHECKING

from rich.console import RenderableType

from textual import messages, on
from textual.app import App, ReturnType
from textual.binding import Binding
from textual.screen import Screen

from sk_aio.cli import AllInOneProvider, Settings, SETTINGS, CSS_PATH
from sk_aio.cli.screens import (
    PluginSelectScreen,
    PluginArgumentScreen,
    PluginOutputScreen
)
from sk_aio.cli.messages import *
from sk_aio.models.events import *

if TYPE_CHECKING:
    from sk_aio.core import AppContext

class AllInOne(App[None]):
    ALLOW_SELECT = False
    AUTO_FOCUS = None
    COMMANDS = { AllInOneProvider }
    CSS_PATH = CSS_PATH
    BINDING_GROUP_TITLE = 'Global Keybinds'
    BINDINGS = [
        Binding(
            'ctrl+q',
            'app.quit',
            description='Quit',
            tooltip='Quit the application',
            priority=True,
            id='quit'
        ),
    ]

    _app_context: 'AppContext'

    def __init__(
        self,
        settings: Settings,
        context: 'AppContext',
    ) -> None:
        SETTINGS.set(settings)

        self.settings = settings
        self._app_context = context
        self.current_screen = None

        super().__init__()

    @property
    def context(self):
        return self._app_context

    def get_default_screen(self) -> Screen:
        self.current_screen = PluginSelectScreen()
        return self.current_screen

    def exit(
        self,
        result: Optional[ReturnType] = None,
        return_code: int = 0,
        message: Optional[RenderableType] = None,
    ) -> None:
        """Exit the app, and return the supplied result.

        Args:
            result: Returned value
            return_code: Application return code, non-zero values indicate a error code.
            message: Message to display on exit
        """

        # TODO: Also stop the event loop here

        self._exit = True
        self._return_value = result # type: ignore
        self._return_code = return_code
        self.post_message(messages.ExitApp())

        if message:
            self._exit_renderables.append(message)
            self._exit_renderables = list(set(self._exit_renderables))

# region Messages
    @on(SwitchToPluginSelectScreen)
    def handle_switch_to_plugin_select_screen(self, message: SwitchToPluginSelectScreen) -> None:
        """Handle switching to the Plugin Select screen."""
        new_screen = self.get_default_screen()
        self.switch_screen(new_screen)
        logging.getLogger(__name__).info("Screen switched to 'PluginScreen'.")

    @on(SwitchToActionArgumentsScreen)
    def handle_switch_to_action_arguments_screen(self, message: SwitchToActionArgumentsScreen) -> None:
        """Handle switching to the Action Arguments screen."""
        new_screen = PluginArgumentScreen(action=message.action)
        self.current_screen = new_screen
        self.push_screen(new_screen)
        self.switch_screen(new_screen)
        logging.getLogger(__name__).info("Screen switched to 'ArgumentScreen'.")

    @on(SwitchToPluginOutputScreen)
    async def handle_switch_to_plugin_output_screen(self, message: SwitchToPluginOutputScreen) -> None:
        """Handle switching to the Plugin Output screen."""
        new_screen = PluginOutputScreen(action=message.action)
        self.current_screen = new_screen
        self.push_screen(new_screen)
        self.switch_screen(new_screen)
        logging.getLogger(__name__).info("Screen switched to 'PluginOutputScreen'.")
        await new_screen.start_action()
# endregion

# region Actions
    async def action_quit(self) -> None:
        """Action to quit the application."""
        bus = self.context.event_bus
        await bus.stop()

        self.exit()
# endregion

# region Event handlers
    def handle_log(
        self,
        event: AppLogEvent | PluginLogEvent
    ) -> None:
        logging.getLogger(__name__).handle(event.message)
        if isinstance(self.current_screen, PluginOutputScreen):
            self.current_screen.post_message(
                AppUpdateLog(event)
            )

    def handle_action_progress(self, event: ActionProgressEvent) -> None:
        if isinstance(self.current_screen, PluginOutputScreen):
            self.current_screen.post_message(
                ActionProgressMessage(event.plugin, event.action, event.progresss)
            )

    def handle_action_error(self, event: ActionErrorEvent) -> None:
        logging.getLogger(__name__).handle(event.message)
        if isinstance(self.current_screen, PluginOutputScreen):
            self.current_screen.post_message(
                ActionErrorMessage(event.plugin, event.action, event.message)
            )
            self.current_screen.post_message(
                AppUpdateLog(
                    PluginLogEvent(
                        plugin=event.plugin,
                        action=event.action,
                        message=event.message
                    )
                )
            )

    def handle_action_complete(self, event: ActionCompleteEvent) -> None:
        if isinstance(self.current_screen, PluginOutputScreen):
            self.current_screen.post_message(
                ActionCompleteMessage(event.plugin, event.action, event.result)
            )
# endregion
