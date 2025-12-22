import os
from pathlib import Path
import sys
import logging

import click
from click_default_group import DefaultGroup
from bubus import EventBus

from sk_aio.cli import AllInOne, Settings
from sk_aio.cli.events import register_events
from sk_aio.core import WorkerManager, PluginLoader
from sk_aio.core.context import AppContext

@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli():
    """A TUI for using Serwis Kacperek's plugins"""

@cli.command()
def default(
    env: tuple[str, ...] = (),
) -> None:
    context = AppContext(
        worker_manager=WorkerManager(),
        plugin_loader=PluginLoader(),
        event_bus=EventBus(),
    )

    app = make_app(context, env)
    app.run()

def make_app(
    context: AppContext,
    env: tuple[str, ...] = (),
) -> AllInOne:
    """Return a SK-AIO instance."""

    if not env and os.path.exists(".env"):
        env = (".env", )

    env_paths = (Path(e).resolve() for e in env)
    settings = Settings(_env_file=env_paths) # type: ignore[call-arg]

    plugins_path = Path(__file__).parent / "plugins"
    context.plugin_loader.load_plugins(plugins_path)

    context.worker_manager.context = context

    app = AllInOne(settings, context=context)
    register_events(app, context.event_bus)

    return app

if __name__ == "__main__":
    cli()
