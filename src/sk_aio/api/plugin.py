from typing import (
    Protocol,
    Callable,
    Any,
    Optional,
    Set,
    overload,
    runtime_checkable,
    TYPE_CHECKING
)

from sk_aio.api import PluginAction

if TYPE_CHECKING:
    from pyproject_parser.type_hints import DependencyGroupsDict

@runtime_checkable
class Plugin(Protocol):
    id: str
    name: str

    deps: Set['DependencyGroupsDict'] = set()
    plugin_deps: Set['DependencyGroupsDict'] = set()    

    def __init__(
        self,
        id: str = "",
        name: str = ""
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

    def get_action(
        self,
        name: str
    ) -> Optional[PluginAction]: ...
