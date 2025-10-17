from typing import Literal, Optional

from textual.app import ComposeResult
from textual.widgets import TextArea
from textual.containers import Vertical

class ReadOnlyTextArea(TextArea):
    """
    A read-only TextArea widget.
    """

    def __init__(
        self,
        text: str = "",
        *,
        language: str | None = None,
        theme: str = "css",
        soft_wrap: bool = True,
        tab_behavior: Literal["focus"] | Literal["indent"] = "focus",
        read_only: bool = True,
        show_line_numbers: bool = False,
        max_checkpoints: int = 50,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            text,
            language=language,
            theme=theme,
            soft_wrap=soft_wrap,
            tab_behavior=tab_behavior,
            read_only=read_only,
            show_line_numbers=show_line_numbers,
            max_checkpoints=max_checkpoints,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

class TextEditor(Vertical):

    def __init__(
        self,
        text_area: TextArea,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
        disabled: bool = False
    ) -> None:
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.text_area = text_area

    def compose(self) -> ComposeResult:
        yield self.text_area

    @property
    def text(self) -> str:
        return self.text_area.text
