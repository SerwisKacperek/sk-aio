from bubus import EventBus

from sk_aio.cli import AllInOne
from sk_aio.models.events import *

def register_events(
    app: AllInOne,
    bus: EventBus
) -> None:
    bus.on(AppLogEvent, app.handle_log)
    bus.on(PluginLogEvent, app.handle_log)
    bus.on(ActionProgressEvent, app.handle_action_progress)
    bus.on(ActionErrorEvent, app.handle_action_error)
    bus.on(ActionCompleteEvent, app.handle_action_complete)
