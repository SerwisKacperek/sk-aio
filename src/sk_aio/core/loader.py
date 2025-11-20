from typing import List, Set
from pathlib import Path
import importlib.util
import logging

import pyproject_parser as ppp

from sk_aio.api import Plugin
from sk_aio.models import BasePlugin

class PluginLoader:
    blacklisted_paths: List[str] = [
        "__pycache__"
    ]

    def __init__(
        self
    ) -> None:
        self._loaded_plugins: Set[Plugin] = []

    # TODO: Implement a loader method to load plugins from `plugins/` directory
    # TODO: Implement a loader method to load plugins using entry points from installed packages

    def _load_pyproject(
        self,
        path: Path,
    ) -> ppp.PyProject:
        # TODO: PyProjectDeprecationWarning

        if path.is_dir():
            path = path / 'pyproject.toml'

        project = ppp.PyProject.load(path) 

        return project
    
    def _load_plugin_from_package(
        self,
        path: Path,
    ) -> Plugin | None:
        """
        Loads a plugin from the specified package directory.
        Args:
            path (Path): The path to the package directory containing the plugin.
        Returns:
            tuple:
                - Plugin: The loaded plugin instance.
                - Set[ppp.DependencyGroupsDict]: A set of dependency groups required by the plugin.
                - Set[ppp.DependencyGroupsDict]: A set of plugin dependency groups required by the plugin.
        Raises:
            ValueError: If the provided path is not a directory.
        """
        if not path.is_dir():
            logging.getLogger(__name__).warning(f"Provided path '{path}' is not a directory.")
            return None
        
        plugin_instance: Plugin = None
        pyproject: ppp.PyProject = None

        # load plugin metadata
        if (path / "pyproject.toml").exists():
            pyproject = self._load_pyproject(path)
        else:
            logging.getLogger(__name__).warning("'%s/pyproject.toml' was not found!", path)
        # try to load the plugin itself
        plugin_file = path / "plugin.py"
        if not plugin_file.exists():
            return None

        module_name = f"{path.name}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        if spec is None or spec.loader is None:
            return None

        # execute the module and create the 'Plugin' object
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not Plugin:
                plugin_instance = attr()
                
        if pyproject and pyproject.dependency_groups:
            if 'external' in pyproject.dependency_groups:
                plugin_instance.deps = pyproject.dependency_groups['external']
            if 'plugins' in pyproject.dependency_groups:
                plugin_instance.plugin_deps = pyproject.dependency_groups['plugins']

        return plugin_instance

    def load_files(
        self,
        plugin_root_path: Path
    ) -> Set[Plugin]:
        plugins: Set[Plugin] = set()

        # TODO: Install dependencies using pip
        # TODO: Add dep's starting with sk_aio to a collection

        for file in plugin_root_path.iterdir():
            # TODO: Implement loading from different structures

            if file.name in self.blacklisted_paths:
                continue

            else:
                if file.is_dir():
                    p = self._load_plugin_from_package(file)
                    plugins.add(p)

        # TODO: Install deps

        return plugins

    def load_plugins(
        self,
        plugin_root_path: Path
    ) -> Set[Plugin]:
        plugins: Set[Plugin] = []

        plugins += self.load_files(plugin_root_path)
        plugins = [plugin for plugin in plugins if plugin is not None]

        self._loaded_plugins = plugins
        return plugins

    @property
    def loaded_plugins(self) -> Set[Plugin]:
        return self._loaded_plugins

    @property
    def loaded_plugin_count(self) -> int:
        return len(self._loaded_plugins)
