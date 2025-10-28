from typing import Optional
import logging
import os
from pathlib import Path

from textual.logging import TextualHandler

from sk_aio.core.logging import BufferedHandler, CustomTextLogFormatter

formatter = CustomTextLogFormatter()

def create_log_file(path: Optional[Path] = None) -> Path:
    if path is None:
        path = os.path.join(os.path.dirname(__file__), '../../logs')
    
    os.makedirs(path, exist_ok=True)

    log_file = os.path.join(path, 'log.log')
    old_log_file = os.path.join(path, 'log-old.log')
    
    if os.path.exists(old_log_file):
        os.remove(old_log_file)
    if os.path.exists(log_file):
        os.rename(log_file, os.path.join(path, 'log-old.log'))

    return log_file

log_file = create_log_file()
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)

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