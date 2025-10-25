import os
import logging
# from enum import Enum, auto

from textual.logging import TextualHandler

from sk_aio.core.logging import BufferedHandler, CustomTextLogFormatter

formatter = CustomTextLogFormatter()

# TODO: Don't hardcode log file path
log_dir = os.path.join(os.path.dirname(__file__), '../..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)

buffered_handler = BufferedHandler()
buffered_handler.setFormatter(formatter)

logging.basicConfig(
    level="NOTSET",
    handlers=[
        TextualHandler(),
    ],
)

logger = logging.getLogger(None)
logger.addHandler(file_handler)
logger.addHandler(buffered_handler)
