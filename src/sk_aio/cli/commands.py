from typing import TYPE_CHECKING, cast

from textual.command import Provider
from textual.types import IgnoreReturnCallbackType

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne

class AllInOneProvider(Provider):
    @property
    def all_in_one_app(self) -> "AllInOne":
        return cast("AllInOne", self.screen.app)

    @property
    def commands(
        self,
    ) -> tuple[tuple[str, IgnoreReturnCallbackType, str, bool], ...]:
        app = self.all_in_one_app
        screen = self.screen

        commands_to_show: list[tuple[str, IgnoreReturnCallbackType, str, bool]] = []

        # TODO: Append commands here based on the current screen
        from sk_aio.cli.screens import PluginSelectScreen # type: ignore[import]
        if isinstance(screen, PluginSelectScreen):
            # TODO: Refresh screen
            # TODO: Search
            # TODO: Run
            pass

        commands_to_show.append(
            (
                "app: Quit SK-AIO",
                app.action_quit,
                "Quit the application and return to the command line",
                True,
            ),
        )

        return tuple(commands_to_show)
