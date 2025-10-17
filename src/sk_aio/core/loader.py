from typing import List
from pathlib import Path
import importlib.util

from sk_aio.models import BasePlugin

class PluginLoader:
    def __init__(
        self
    ) -> None:
        self._loaded_plugins: List[BasePlugin] = []

    def load_plugins(
        self,
        plugin_root_path: Path
    ) -> List[BasePlugin]:
        plugins: List[BasePlugin] = []

        for folder in plugin_root_path.iterdir():
            if not folder.is_dir():
                continue

            plugin_file = folder / "plugin.py"
            if not plugin_file.exists():
                continue

            module_name = f"plugins.{folder.name}.plugin"
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec is None or spec.loader is None:
                continue

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not BasePlugin:
                    plugin_instance: BasePlugin = attr()
                    plugins.append(plugin_instance)

        self._loaded_plugins = plugins
        return plugins

    @property
    def loaded_plugins(self) -> List[BasePlugin]:
        return self._loaded_plugins

    @property
    def loaded_plugin_count(self) -> int:
        return len(self._loaded_plugins)
