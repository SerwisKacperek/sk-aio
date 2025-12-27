from typing import Protocol, Callable, Any, Optional, TYPE_CHECKING, runtime_checkable
from abc import abstractmethod

from sk_aio.api import PluginActionArgument, PluginAPI

if TYPE_CHECKING:
    from sk_aio.api import Plugin
    from sk_aio.models import BasePlugin

@runtime_checkable
class PluginAction(Protocol):
    name: str
    description: Optional[str]
    dependencies: dict[str, set[str]]

    def __init__(
        self,
        plugin: object,
        name: str,
        method: Callable[..., Any] = lambda *args, **kwargs: None,
        description: Optional[str] = None,
        args: Optional[list[PluginActionArgument[Any]]] = None,
    ) -> None: ...

    @property
    def method(self) -> Callable[..., Any]: ...

    @property
    def plugin(self) -> 'Plugin': ...

    @property
    def args(self) -> list[PluginActionArgument[Any]]: ...

    @abstractmethod
    async def execute(
        self,
        api: PluginAPI,
        *args,
        **kwargs
    ) -> Any: ...
