from typing import List
from logging import Handler, LogRecord, Formatter

class CustomTextLogFormatter(Formatter):
    def __init__(
        self,
        fmt: str = "[%(levelname)s]%(plugin)s.%(action)s: %(message)s",
        datefmt: str = "%H:%M:%S",
        style: str = '%',
        validate: bool = True,
    ) -> None:
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style=style,  # type: ignore
            validate=validate,
            defaults={
                'plugin': None,
                'action': None,
            },
        )

    def formatMessage(self, record: LogRecord) -> str:
        output = f"[{record.levelname}]"

        if hasattr(record, "plugin") and record.plugin is not None: # type: ignore
            output += record.plugin # type: ignore
            if hasattr(record, "action") and record.action is not None: # type: ignore
                output += f".{record.action}" # type: ignore
        else:
            output += f"{record.name}"

        output += ": "
        output += record.getMessage()
        return output

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
        self._buffer: List[LogRecord] = [] # TODO: Change into a collection

    def emit(
        self,
        record: LogRecord
    ) -> None:
        self.buffer.append(record)

    @property
    def buffer(self) -> List[LogRecord]:
        return self._buffer

    @buffer.setter
    def buffer(self, new_value: List[LogRecord]) -> None:
        self._buffer = new_value

        if len(self._buffer) > self.capacity:
            self._buffer.pop(0)
