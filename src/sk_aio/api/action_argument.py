from dataclasses import dataclass
from typing import Type, TypeVar, Optional

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