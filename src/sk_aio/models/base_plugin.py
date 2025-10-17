from dataclasses import dataclass
from typing import Optional, List, Type, TypeVar, Any, Callable, overload, TYPE_CHECKING

if TYPE_CHECKING:
    from sk_aio.models.plugin_api import PluginAPI

T = TypeVar("T")

@dataclass
class PluginActionArgument[T]:
    name: str
    required: bool
    type: Type[T]
    group: Optional[str] = None
    description: Optional[str] = None
    default_value: Optional[T] = None
    value: Optional[T] = None

class PluginAction:
    def __init__(
        self,
        name: str,
        method: Callable[..., Any],
        plugin: "BasePlugin",
        description: Optional[str] = None,
        args: Optional[List[PluginActionArgument[Any]]] = None,
    ) -> None:
        self.name = name
        self.method = method
        self.plugin = plugin
        self.description = description
        self.args = args or []

    def execute(
        self,
        **kwargs,
    ) -> Any:
        for arg in self.args:
            if arg.required and arg.name not in kwargs:
                raise ValueError(f"Missing required argument: {arg.name}")
        return self.method(**kwargs)

class BasePlugin:
    id: str
    name: str
    actions: List[PluginAction]

    def __init__(
        self,
        id: str = "",
        name: str = "",
    ) -> None:
        self.id = id
        self.name = name
        self.actions = []

    @overload
    def register_action(
        self,
        name: str,
        method: Callable[..., Any],
        args: Optional[List[PluginAction]] = None,
    ) -> PluginAction: ...

    @overload
    def register_action(
        self,
        action: PluginAction
    ) -> PluginAction: ...

    def register_action(self, *args, **kwargs) -> PluginAction:
        if len(args) == 1 and isinstance(args[0], PluginAction):
            action = args[0]
        else:
            name = kwargs.get('name', args[0] if len(args) > 0 else None)
            method = kwargs.get('method', args[1] if len(args) > 1 else None)
            action_args = kwargs.get('args', args[2] if len(args) > 2 else None)

            if name is None:
                raise ValueError("Action name cannot be empty!")
            if method is None:
                raise ValueError("Method cannot be empty!")

            action = PluginAction(name, method, plugin=self, args=action_args)

        self.actions.append(action)
        return action

    def get_action(
        self,
        name: str
    ) -> Optional[PluginAction]:
        return next((a for a in self.actions if a.name == name), None)

    def exec_action(self, action: PluginAction, **kwargs) -> None:
        return action.execute(**kwargs)

    def configure_action(self, action: PluginAction) -> PluginAction: ...
