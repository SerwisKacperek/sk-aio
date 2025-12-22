from typing import Protocol, Callable, Any, Optional, TypeVar, TYPE_CHECKING, runtime_checkable

from sk_aio.api import PluginActionArgument, PluginAPI

if TYPE_CHECKING:
    from sk_aio.api import Plugin

T = TypeVar("T")

@runtime_checkable
class PluginAction(Protocol):
    # TODO: Find a way to type this without defining as ClassVars
    name: str
    method: Callable[..., Any]
    plugin: 'Plugin'
    description: Optional[str]
    args: list[PluginActionArgument[Any]]

    dependencies: dict[str, set[str]]

    def __init__(
        self,
        name: str,
        method: Callable[..., Any],
        plugin: 'Plugin',
        description: Optional[str] = None,
        args: Optional[list[PluginActionArgument[Any]]] = None,
    ) -> None: ...

    @staticmethod
    def get_dependency(obj) -> Optional[T]:
        pass

    async def execute(
        self,
        api: PluginAPI,
        *args,
        **kwargs
    ) -> Any: ...
