from typing import List, Set
from pathlib import Path
import importlib.util
from importlib.metadata import distributions
import logging
import subprocess
import sys

import pyproject_parser as ppp
from dom_toml.parser import BadConfigError
import networkx as nx

from sk_aio.api import Plugin
from sk_aio.models import BasePlugin

class PluginLoader:
    blacklisted_paths: List[str] = [
        "__pycache__",
        "__init__.py",
    ]

    def __init__(
        self,
    ) -> None:
        self._lodaed_plugins: Set[Plugin] = set()

    @staticmethod
    def resolve_dependencies(
        config: tuple[Path, ppp.PyProject],
    ) -> None:
        if config[1].dependency_groups is None or config[1].dependency_groups['external'] is None:
            return # no external dependencies to install

        # Ignore DependencyGroupDict objects for now
        already_installed_packages = {dist.metadata['Name'].lower() for dist in distributions() if 'Name' in dist.metadata}
        external_packages = [
            pkg for pkg in config[1].dependency_groups['external']
            if isinstance(pkg, str) and pkg.lower().split('==')[0] not in already_installed_packages
        ]

        if len(external_packages) == 0:
            return
        logging.getLogger(__name__).debug(
            "Installing \"%s\" for %s plugin",
            " ".join(external_packages),
            config[1].project['name']
        )

        (status, output) = subprocess.getstatusoutput(
            [sys.executable, "-m", "pip", "install"] + external_packages
        )
        if status != 0:
            raise RuntimeError(output)
        logging.getLogger(__name__).debug(output)

        return

    @staticmethod
    def resolve_plugin_dependencies(
        config: tuple[Path, ppp.PyProject],
    ) -> bool:
        # Returns True if plugin can safely load (all deps loaded)
        if config[1].dependency_groups is None or config[1].dependency_groups['plugins'] is None:
            return True # no plugins dependencies

        active_plugins = PluginLoader.get_active_plugins()
        active_plugins = [ap.split('.')[-1] for ap in active_plugins]

        for dep in config[1].dependency_groups['plugins']:
            if dep not in active_plugins:
                return False

        return True

    @staticmethod
    def get_active_plugins() -> set[str]:
        result: set[str] = set()

        for name in sys.modules:
            if "sk_aio.plugins." in name:
                if name.find('.actions') == -1:
                    result.add(name)

        return result

    @property
    def loaded_plugins(self) -> Set[Plugin]:
        return self._lodaed_plugins

    @property
    def loaded_plugin_count(self) -> int:
        return len(self._lodaed_plugins)

    def load_plugins(
        self,
        plugin_root_path: Path,
    ) -> Set[Plugin]:

        configs = self._load_plugin_configs(plugin_root_path)
        configs = self._sort_load_order(configs)

        # TODO: Add a setting to auto install dependencies or skip loading those plugins
        # Resolve external dependencies
        for config in configs:
            try:
                PluginLoader.resolve_dependencies(config)
            except RuntimeError as error:
                logging.getLogger(__name__).error(
                    "Error occured while trying to install dependencies for \"%s\" plugin: %s", 
                    config[1].project['name'],
                    error
                )

        self._lodaed_plugins = self._load_plugins(configs)

        return self.loaded_plugins

    def _load_pyproject(
        self,
        path: Path,
    ) -> ppp.PyProject | None:
        if path.is_dir():
            path = path / "pyproject.toml"

        try:
            project = ppp.PyProject.load(path)
        except BadConfigError:
            logging.getLogger(__name__).error("Failed to load pyproject.toml from %s", path)
            return None

        return project

    def _load_plugin_configs(
        self,
        plugin_root_path: Path,
    ) -> List[tuple[Path, ppp.PyProject]]:
        plugin_configs: List[tuple[Path, ppp.PyProject]] = []

        for file in plugin_root_path.iterdir():
            if file.name in self.blacklisted_paths:
                continue
            pyproject: ppp.PyProject | None = None

            # Load plugin as a package
            if file.is_dir():
                if (file / "pyproject.toml").exists():
                    pyproject = self._load_pyproject(file)
                else:
                    logging.getLogger(__name__).warning("'%s/pyproject.toml' was not found!", file)

            if pyproject is not None and pyproject.project is not None:
                plugin_configs.append((file, pyproject))
            else:
                logging.getLogger(__name__).warning("Could not load plugin config for '%s'", file)

        return plugin_configs

    def _sort_load_order(
        self,
        plugin_configs: List[tuple[Path, ppp.PyProject]]
    ) -> List[tuple[Path, ppp.PyProject]]:
        g = nx.DiGraph()
        name_to_plugin: dict[str, tuple[Path, ppp.PyProject]] = {}

        for plugin in plugin_configs:
            if plugin[1].project is None or plugin[1].project["name"] is None:
                logging.getLogger(__name__).warning("Plugin at '%s' not loaded due to missing or invalid pyproject.", plugin[0])
                continue

            name_to_plugin[plugin[1].project["name"]] = plugin

        for plugin in plugin_configs:
            if plugin[1].project is None or plugin[1].project["name"] is None:
                continue

            g.add_node(plugin[1].project["name"])

            # If no plugin dependencies, continue
            dependencies = plugin[1].project.get("dependencies")
            plugin_deps = dependencies.get("plugins") if isinstance(dependencies, dict) else None
            if not dependencies or not plugin_deps:
                continue

            for dep in plugin_deps:
                g.add_edge(plugin[1].project["name"], dep)

        while not nx.is_directed_acyclic_graph(g):
            try:
                cycle = nx.find_cycle(g)
                plugin_to_remove = cycle[0][0]
                logging.error("Circular plugin dependency detected! Removing plugin: %s", plugin_to_remove)

                g.remove_node(plugin_to_remove)
                if plugin_to_remove in name_to_plugin:
                    del name_to_plugin[plugin_to_remove]
            except nx.NetworkXNoCycle:
                break

        sorted_names = list(nx.topological_sort(g))
        return [name_to_plugin[name] for name in sorted_names if name in name_to_plugin]

    def _load_plugin_from_package(
        self,
        package_path: Path,
    ) -> Plugin | None:
        if not package_path.is_dir():
            logging.getLogger(__name__).warning("Provided path '%s' is not a directory.", str(package_path))
            return None

        plugin_instance: Plugin | None = None

        plugin_instance: Plugin | None = None

        # try to load the plugin itself
        plugin_file = package_path / "plugin.py"
        if not plugin_file.exists():
            return None

        module_name = f"{package_path.name}"
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

        if not plugin_instance:
            return None

        return plugin_instance

    def _load_plugins(
        self,
        plugin_configs: List[tuple[Path, ppp.PyProject]],
    ) -> Set[Plugin]:
        plugins: Set[Plugin] = set()

        for config in plugin_configs:
            plugin_instance: Plugin | None = None

            if not PluginLoader.resolve_plugin_dependencies(config):
                logging.getLogger(__name__).error(
                    "Required plugin dependencies for \"%s\" are missing. Skipping plugin. \"%s\"",
                    config[1].project['name'],
                    config[1].dependency_groups['plugins']
                )
                plugin_configs.remove(config)

            if config[0].is_dir():
                plugin_instance = self._load_plugin_from_package(config[0])

            if plugin_instance is None:
                continue
            plugins.add(plugin_instance)

        return plugins
