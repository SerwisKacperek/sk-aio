from typing import overload
import asyncio
import threading
import logging

from bubus import EventBus

from sk_aio.models import BasePlugin, PluginAction, PluginAPI

class WorkerManager:
    bus: 'EventBus'

    def __init__(
        self,
        event_bus: 'EventBus',
    ) -> None:
        self.bus = event_bus

    @overload
    def run_action(
        self,
        plugin: BasePlugin,
        action: str,
    ) -> None: ...

    @overload
    def run_action(
        self,
        plugin: BasePlugin,
        action: PluginAction,
    ) -> None: ...

    def run_action(
        self,
        plugin: BasePlugin,
        action: str | PluginAction,
        **kwargs,
    ) -> None:
        api = PluginAPI(
            self.bus,
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

        method = action.method
        method_args = {}
        for arg in action.args:
            method_args[arg.name] = getattr(arg, "value", None) if getattr(arg, "value", None) is not None else getattr(arg, "default_value", None)

        def run_sync():
            logging.getLogger(__name__).debug(f"Starting sync action '{action.name}' ...")
            method(api, **method_args, **kwargs)
            api.complete()

        def run_async():
            logging.getLogger(__name__).debug(f"Starting async action '{action.name}' ...")
            asyncio.run(method(api, **method_args, **kwargs))

        if asyncio.iscoroutinefunction(method):
            threading.Thread(target=run_async, daemon=True).start()
        else:
            threading.Thread(target=run_sync, daemon=True).start()
