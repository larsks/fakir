import uasyncio as asyncio
import gc
import json
import machine
import network
import os
import time

from snakecharmer import logging
from snakecharmer import utils
from snakecharmer import webserver

gc.collect()


class WebApp(webserver.Webserver):
    connect_timeout = 30000
    mode = 'control'

    def __init__(self, loop):
        super().__init__(loop)

        self.add_route('/', self.index)

    async def index(self, reader, writer, req):
        await self.send_file(
            writer, '/static/status.html')


def init_tasks(loop):
    ws = WebApp(loop)

    t_webserver = asyncio.start_server(
        ws.handle_request, '0.0.0.0', 80)

    return [t_webserver]