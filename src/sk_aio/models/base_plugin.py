from typing import (
    TypeVar,
    Any,
    Callable,
    Optional,
    List,
)

from sk_aio.api import PluginAPI, Plugin, PluginAction, PluginActionArgument


T = TypeVar("T", bound='PluginAction')

class BasePluginAction(PluginAction):
    _method: Callable[..., Any] = lambda *args, **kwargs: None
    _plugin: 'Plugin'
    _args: list[PluginActionArgument[Any]] = []
    dependencies: dict[str, set[str]] = {}

    def __init__(
        self,
        plugin: "BasePlugin",
        name: str,
        method: Callable[..., Any],
        description: Optional[str] = None,
        args: Optional[List[PluginActionArgument[Any]]] = None,
    ) -> None:
        self.name = name
        self.description = description

        self._method = method
        self._plugin = plugin
        self._args = args or list()

    @property
    def method(self) -> Callable[..., Any]:
        return self._method

    @property
    def plugin(self) -> 'Plugin':
        return self._plugin

    @property
    def args(self) -> list[PluginActionArgument[Any]]:
        return self._args

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
            mth = self.method
            result = await mth(api, **kwargs)
        except Exception as e:
            api.error(f"An error occured when running the action...\n{e}")
            raise e
        else:
            api.complete()
            return result

class BasePlugin(Plugin):
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

            action = BasePluginAction(self, name, method, args=action_args)

        self.actions.append(action)
        return action

    def get_action(
        self,
        name: str
    ) -> Optional[PluginAction]:
        return next((a for a in self.actions if getattr(a, 'name', None) == name), None)

    def configure_action(self, action: PluginAction) -> PluginAction: ...

def depends_on_action(
        plugin_name: str,
        action_name: str
    ) -> Callable[[type[T]], type[T]]:

    def decorator(cls: type[T]) -> type[T]:
        if plugin_name not in cls.dependencies:
            cls.dependencies[plugin_name] = set()
        cls.dependencies[plugin_name].add(action_name)
        return cls
    return decorator
