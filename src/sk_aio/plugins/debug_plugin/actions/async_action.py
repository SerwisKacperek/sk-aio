from typing import TYPE_CHECKING
import logging
import time
import random

from sk_aio.api import PluginAPI
from sk_aio.models import BasePluginAction

if TYPE_CHECKING:
    from ..plugin import DebugPlugin

class AsyncAction(BasePluginAction):
    def __init__(self, plugin: 'DebugPlugin') -> None:
        super().__init__(
            name="async_action",
            description="Sleep for a random amount of time.",
            method=self.run,
            plugin=plugin,
            args=None
        )

    async def run(self, api: PluginAPI) -> None:
        api.log("Going for a quick nap a few times...", level=logging.INFO)
        for i in range(3):
            nap_time = random.randint(1,5)
            time.sleep(nap_time)
            api.log("Went to sleep for "+str(nap_time)+" seconds.")
        api.log("Nap time over.")
        return
