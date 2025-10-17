from textual.app import ComposeResult
from textual.widgets import Label
from textual.containers import Vertical, Horizontal

from sk_aio.cli.config import SETTINGS
from sk_aio.cli.version import VERSION

class AppHeader(Horizontal):
    """Header bar container for the application"""

    def compose(self) -> ComposeResult:
        settings = SETTINGS.get().heading

        if settings.show_version:
            yield Label(f"[b]SK-AIO [dim]{VERSION}[/]", id='app-title')
        else:
            yield Label("[b]SK-AIO", id='app-title')

        self.set_class(not settings.visible, "hidden")

class AppBody(Vertical):
    """Application's body container"""
