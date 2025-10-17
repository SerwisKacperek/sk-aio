"""Module for generic widgets"""

from typing import Generic, TypeVar

from textual.widgets import ListItem

T = TypeVar("T")

class GenericListItem(Generic[T], ListItem):
    model: T

    def __init__(self, model: T, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = model
