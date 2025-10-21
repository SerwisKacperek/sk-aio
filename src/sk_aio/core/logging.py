from typing import List, Any
from logging import Handler, LogRecord, Formatter

class CustomTextLogFormatter(Formatter):
    def __init__(
        fmt: str = "%(message)s",
        datefmt: str = "%H:%M:%S",
        style: str = "{",
        validate: bool = True,
        *,
        defaults: dict[str, Any] = {
            "plugin": None,
            "action": None,
        },
    ) -> None:
        super().__init__(
            fmt,
            datefmt,
            style,
            validate,
            defaults
        )

class BufferedHandler(Handler):
    """
    A logger handler that stores a number of the last log messages in a buffer.
    """
    def __init__(
        self,
        capacity=100
    ) -> None:
        super().__init__()
        self.capacity = capacity
        self._buffer = [] # TODO: Change into a collection

    def emit(
        self,
        record: LogRecord
    ) -> None:
        message = self.format(record)
        self.buffer.append(message)

    @property
    def buffer(self) -> List[str]:
        return self._buffer

    @buffer.setter
    def buffer(self, new_value: List[str]) -> None:
        self._buffer = new_value

        if len(self._buffer) > self.capacity:
            self._buffer.pop(0)
