from typing import overload
import asyncio
import threading
import logging

from bubus import EventBus

from sk_aio.api import Plugin, PluginAction
from sk_aio.models import BaseAPI

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

        method_args = {}
        for arg in action.args:
            method_args[arg.name] = getattr(arg, "value", None) if getattr(arg, "value", None) is not None else getattr(arg, "default_value", None)

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
