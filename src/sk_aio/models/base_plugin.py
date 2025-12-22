from typing import (
    TypeVar,
    Any,
    Callable,
    Optional,
    List,
)

from sk_aio.api import PluginAPI, Plugin, PluginAction, PluginActionArgument

T = TypeVar("T", bound=PluginAction)

class BasePluginAction(PluginAction):
    name: str
    method: Callable[..., Any]
    plugin: 'Plugin'
    description: Optional[str]
    args: list[PluginActionArgument[Any]]

    dependencies: dict[str, set] = {}

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
        self.args = args or list()

    async def execute(
        self,
        api: PluginAPI,
        *args,
        **kwargs,
    ) -> Any:
        for arg in self.args:
            if arg.required and arg.name not in kwargs:
                raise ValueError(f"Missing required argument: {arg.name}")

        try:
            result = await self.method(api, **kwargs)
        except Exception as e:
            api.error(f"An error occured when running the action...\n{e}")
            raise e
        else:
            api.complete()
            return result

class BasePlugin(Plugin):
    id: str
    name: str

    def __init__(
        self,
        id: str = "",
        name: str = "",
    ) -> None:
        self.id = id
        self.name = name
        self.actions = []

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

            action = BasePluginAction(name, method, plugin=self, args=action_args)

        self.actions.append(action)
        return action

    def get_action(
        self,
        name: str
    ) -> Optional[PluginAction]:
        return next((a for a in self.actions if getattr(a, 'name', None) == name), None)

    def configure_action(self, action: PluginAction) -> PluginAction: ...

def depends_on_action(plugin_name: str, action_name: str) -> Callable[[T], T]:
    def decorator(cls: T) -> T:
        if 'dependencies' not in cls.__dict__:
            cls.dependencies = {}
        if plugin_name not in cls.dependencies:
            cls.dependencies[plugin_name] = set()
        cls.dependencies[plugin_name].add(action_name)
        return cls
    return decorator
