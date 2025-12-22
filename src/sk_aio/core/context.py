from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sk_aio.core.worker_manager import WorkerManager
    from sk_aio.core.loader import PluginLoader
    from bubus import EventBus

@dataclass(frozen=True)
class AppContext:
    worker_manager: 'WorkerManager'
    plugin_loader: 'PluginLoader'
    event_bus: 'EventBus'
