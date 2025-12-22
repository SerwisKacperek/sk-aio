from typing import Literal
from unittest.mock import MagicMock
from contextvars import ContextVar

from bubus import EventBus
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from sk_aio.core import WorkerManager, PluginLoader

class HeadingSettings(BaseModel):
    """Settings for the application header bar."""

    visible: bool = Field(default=True)
    show_version: bool = Field(default=True)

class PluginPropertiesSettings(BaseModel):
    """Settings for the PluginProperitesArea widget"""

    position: Literal["left", "right"] = Field(default="left")

class Settings(BaseSettings):
    """Settings model for the SK-AIO application."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="posting_",
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="allow",
    )
    heading: HeadingSettings = Field(default_factory=HeadingSettings)
    plugin_properties: PluginPropertiesSettings = Field(default_factory=PluginPropertiesSettings)

SETTINGS: ContextVar[Settings] = ContextVar("settings")
