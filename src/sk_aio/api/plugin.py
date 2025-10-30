from typing import Protocol, Callable, Any, Optional, overload

from sk_aio.api import PluginAction

class Plugin(Protocol):
    def __init__(
        id: str,
        name: str
    ) -> None: ...

    @overload
    def register_action(
        self,
        name: str,
        method: Callable[..., Any],
        args: Optional[list[PluginAction]] = None,
    ) -> PluginAction: ...

    @overload
    def register_action(
        self,
        action: PluginAction
    ) -> PluginAction: ...
