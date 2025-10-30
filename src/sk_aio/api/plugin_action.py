from typing import Protocol, Callable, Any, Optional, TYPE_CHECKING, runtime_checkable

from sk_aio.api import PluginActionArgument, PluginAPI

if TYPE_CHECKING:
    from sk_aio.api import Plugin

@runtime_checkable
class PluginAction(Protocol):
    def __init__(
        name: str,
        method: Callable[..., Any],
        plugin: 'Plugin',
        description: Optional[str] = None,
        args: Optional[list[PluginActionArgument[Any]]] = None,
    ) -> None: ...

    async def execute(
        api: PluginAPI,
        *args,
        **kwargs
    ) -> Any: ...
