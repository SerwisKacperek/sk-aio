from typing import Set, Any, cast, TYPE_CHECKING

from textual.app import ComposeResult
from textual.widgets import ListView, Label

from sk_aio.api import Plugin, PluginAction
from sk_aio.cli.widgets import GenericListItem

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne

class PluginListItemWidget(GenericListItem[PluginAction]):
    pass

class PluginSelector(ListView):
    """Plugin selector widget for the PluginSelect screen"""

    filters: dict[str, Any] = {}
    plugins: Set[Plugin] = set()

    class Selected(ListView.Selected):
        """
        An override of the ListView.Selected class to provide
        type-safe acces to the selected item
        """
        def __init__(self, list_view: ListView, item: PluginListItemWidget, index: int) -> None:
            super().__init__(list_view, item, index)
            self.list_view: ListView = list_view
            self.item: PluginListItemWidget = item # type: ignore
            self.index: int = index

        @property
        def model(self) -> PluginAction:
            return self.item.model

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.all_in_one_app = cast('AllInOne', self.app)
        self.plugins = self.all_in_one_app.context.plugin_loader.loaded_plugins

    def compose(self) -> ComposeResult:
        for plugin in self.plugins:
            for action in plugin.actions:
                yield PluginListItemWidget(
                    action,
                    Label(f"[#5457FA][dim]{plugin.name}:[/][/]{action.name.upper()}\n"
                          f"[dim]{action.description or ""}[/]")
                )
