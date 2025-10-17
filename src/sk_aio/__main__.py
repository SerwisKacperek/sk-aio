import os
import asyncio
from pathlib import Path

import click
from click_default_group import DefaultGroup
from bubus import EventBus

from sk_aio.cli import AllInOne, Settings
from sk_aio.cli.events import register_events
from sk_aio.core import WorkerManager, PluginLoader

@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli():
    """A TUI for using Serwis Kacperek's plugins"""

@cli.command()
def default(
    env: tuple[str, ...] = (),
) -> None:
    event_bus = EventBus()
    manager = WorkerManager(event_bus=event_bus)

    app = make_app(event_bus, manager, env)
    app.run()

def make_app(
    event_bus: EventBus,
    worker_manager: WorkerManager,
    env: tuple[str, ...] = (),
) -> AllInOne:
    """Return a SK-AIO instance."""

    if not env and os.path.exists(".env"):
        env = (".env", )

    env_paths = (Path(e).resolve() for e in env)
    settings = Settings(_env_file=env_paths) # type: ignore[call-arg]
    settings.event_bus = event_bus
    settings.worker_manager = worker_manager

    plugin_loader = PluginLoader()
    plugins_path = Path(__file__).parent / "plugins"
    plugin_loader.load_plugins(plugins_path)
    settings.plugin_loader = plugin_loader

    app = AllInOne(settings)
    register_events(app, event_bus)

    return app

if __name__ == "__main__":
    cli()
