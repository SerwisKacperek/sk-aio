from typing import overload, TYPE_CHECKING
import asyncio
import threading
import logging

from sk_aio.api import Plugin, PluginAction
from sk_aio.models import BaseAPI

if TYPE_CHECKING:
    from sk_aio.core import AppContext

class WorkerManager:
    context: 'AppContext'

    def get_dependencies(
        self,
        action: PluginAction
    ) -> dict[str, PluginAction | None]:
        loader_instance = self.context.plugin_loader
        actions: dict[str, PluginAction | None] = {}

        if loader_instance is None:
            raise RuntimeError("Plugin loader instance is missing in SETTINGS.")

        for dep in action.dependencies.keys():
            pi = loader_instance.get_active_plugin(dep)

            if pi is None:
                continue

            for act in action.dependencies[dep]:
                actions[act] = pi.get_action(act)

        return actions

    @overload
    def run_action(
        self,
        plugin: Plugin,
        action: str,
    ) -> None: ...

    @overload
    def run_action(
        self,
        plugin: Plugin,
        action: PluginAction,
    ) -> None: ...

    def run_action(
        self,
        plugin: Plugin,
        action: str | PluginAction,
        **kwargs,
    ) -> None:
        api = BaseAPI(
            self.context,
            plugin.id
        )
        if isinstance(action, PluginAction):
            api.current_action = action.name
        else:
            api.current_action = action

            plugin_action: PluginAction | None = plugin.get_action(action)
            if plugin_action is None:
                raise ValueError(f"Action '{action}' not found in plugin '{plugin.name}'")

            api.current_action = plugin_action.name
            action = plugin_action

        deps = self.get_dependencies(action)

        # Add standard arguments
        method_args = {}
        for arg in action.args:
            method_args[arg.name] = getattr(arg, "value", None) if getattr(arg, "value", None) is not None else getattr(arg, "default_value", None)

        # Add dependencies to method_args
        method_args = {**method_args, **deps}

        async def run_sync():
            logging.getLogger(__name__).debug("Starting sync action '%s' ...", action.name)
            try:
                await action.execute(api, **method_args, **kwargs)
            except Exception as e:
                logging.getLogger(__name__).error("Failed to run the action:\n%s", e)

        def run_async():
            logging.getLogger(__name__).debug("Starting async action '%s' ...", action.name)
            try:
                asyncio.run(action.execute(api, **method_args, **kwargs))
            except Exception as e:
                logging.getLogger(__name__).error("Failed to run the action:\n%s", e)

        if asyncio.iscoroutinefunction(action.method):
            threading.Thread(target=run_async, daemon=True).start()
        else:
            threading.Thread(target=run_sync, daemon=True).start()
