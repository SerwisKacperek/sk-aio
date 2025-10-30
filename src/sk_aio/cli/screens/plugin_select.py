from typing import TYPE_CHECKING, cast

from textual import on
from textual.screen import Screen
from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Input

from sk_aio.api import PluginAction
from sk_aio.cli.screens import AppHeader, AppBody
from sk_aio.cli.widgets import (
    PluginSearchBar,
    PluginSelector,
    PluginListItemWidget,
    PluginPropertiesArea,
    GenericListItem
)
from sk_aio.cli.messages import SwitchToActionArgumentsScreen, SwitchToPluginOutputScreen

if TYPE_CHECKING:
    from sk_aio.cli import AllInOne

class PluginSelectScreen(Screen[None]):
    AUTO_FOCUS = "PluginSelector"
    BINDING_GROUP_TITLE = "Plugin Select Screen"

    current_selection: Reactive[
        PluginListItemWidget | None
    ] = reactive(None, init=False, bindings=True)

    def __init__(self) -> None:
        super().__init__()

        self.all_in_one_app = cast("AllInOne", self.app)

    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield PluginSearchBar()

        with AppBody():
            yield PluginSelector()
            yield PluginPropertiesArea()

        yield Footer(show_command_palette=False)

    def watch_current_selection(
        self,
        old_selection: GenericListItem[PluginAction] | None,
        new_selection: GenericListItem[PluginAction]
    ) -> None:
        self.plugin_properties_area.on_selected_plugin(new_selection)

# region Messages
    @on(Input.Submitted, selector="SearchInput")
    def handle_search_change(self) -> None:
        """Update the filter parameters when submitting the 'SearchInput'."""
        self.plugin_selector.filters # TODO: Change the plugin filters here

    @on(PluginSelector.Selected, selector="PluginSelector")
    def handle_select_change(self, event: PluginSelector.Selected) -> None:
        """Update the current selection when this event is captured."""

        # Post the message only if the same element is selected twice
        if self.current_selection == event.item:
            # If the action has no arguments, switch directly to the output screen
            if len(event.item.model.args) == 0:
                self.app.post_message(
                    SwitchToPluginOutputScreen(
                        self,
                        event.item.model
                    )
                )
            else:
                self.app.post_message(
                    SwitchToActionArgumentsScreen(
                        self,
                        event.item.model
                    )
                )

        self.current_selection = event.item
# endregion

# region Properties
    @property
    def app_header(self) -> AppHeader:
        return self.query_one(AppHeader)

    @property
    def app_body(self) -> AppBody:
        return self.query_one(AppBody)

    @property
    def plugin_properties_area(self) -> PluginPropertiesArea:
        return self.query_one(PluginPropertiesArea)

    @property
    def plugin_selector(self) -> PluginSelector:
        return self.query_one(PluginSelector)
# endregion
