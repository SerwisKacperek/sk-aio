from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Label
from textual.containers import Vertical

from sk_aio.models import PluginAction
from sk_aio.cli.widgets import GenericListItem
from sk_aio.cli.config import SETTINGS

class PluginPropertiesArea(Vertical):
    COMPONENT_CLASSES = {
        "border-title-status"
    }

    display_data: list[Widget] = []

    def on_mount(self) -> None:
        self.add_class("section")

    def compose(self) -> ComposeResult:
        self.styles.dock = SETTINGS.get().plugin_properties.position
        self.border_title = "Plugin Properties"

        if len(self.display_data) == 0:
            yield Static(
                "Select a plugin to view it's properties.",
                id="empty-plugin-properties"
            )

        self.mount_all(self.display_data)

    def on_selected_plugin(self, plugin_widget: GenericListItem[PluginAction] | None) -> None:
        self.remove_children()
        self.display_data.clear()

        if plugin_widget is not None:
            self.display_data = [
                Label(
                    f"[bold]{plugin_widget.model.name.upper()}[/]\n"
                    f"[#5457FA]{plugin_widget.model.plugin.name}[/]"
                ),
            ]

            # TODO: Fix the container size
            if plugin_widget.model.description is not None:
                self.display_data.append(
                    Label(f"\n{plugin_widget.model.description}\n")
                )

            arguments = [arg for arg in plugin_widget.model.args]
            if len(arguments) > 0:
                self.display_data.append(Label("\n[bold]Action Arguments[/]\n"))
                for arg in arguments:
                    label_text = f"{arg.name.upper()}:\n"

                    if arg.description:
                        label_text += f"{arg.description}\n"

                    label_text += (
                        f"Required: {arg.required}\n"
                        f"Type: {arg.type}\n"
                        f"Default: {arg.default_value}\n\n"
                    )
                    self.display_data.append(Label(label_text))

        self.mount_all(self.display_data)
