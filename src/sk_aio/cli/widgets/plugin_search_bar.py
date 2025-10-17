from typing import Optional
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Button, Input
from textual.widgets.input import Selection
from textual.message import Message
from textual.containers import Vertical, Horizontal

class PluginSearchFilters(Button):
    pass # TODO: Implement SearchFilters button

class SearchInput(Input):
    BINDING_GROUP_TITLE = "Plugin Search Input"

    BINDINGS = [
        Binding("down", "app.focus_next", "Focus next", show=False),
        Binding("ctrl+a", "select_all", "Select All", show=False),
    ]

    @dataclass
    class CursorMoved(Message):
        cursor_position: int
        value: str
        input: "SearchInput"

        @property
        def control(self) -> "SearchInput":
            return self.input

    def watch_selection(self, selection: Selection) -> None:
        self.post_message(self.CursorMoved(selection.end, self.value, self))

    def action_select_all(self) -> None:
        self.selection = Selection(0, len(self.value))

class PluginSearchBar(Vertical):
    """Search bar widget for the PluginSelectScreen."""

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled
        )

    def compose(self) -> ComposeResult:
        with Horizontal(id='search-row'):
            yield SearchInput(
                placeholder="@p <plugin_name>; @n <action name>; @d <description>",
                id='search-input'
            )
            yield PluginSearchFilters(
                "Filters"
            )

    @property
    def search_input(self) -> "SearchInput":
        return self.query_one("#search-input", SearchInput)
