import socket
import asyncio

from quumremote.terminal import ShittyTerminal
from quumremote.shell import ShittyShell


class ManagedQUUM:
    __slots__ = ['_terminal', '_shell']

    def __init__(self):
        self._terminal = None

    async def connect(self, socket_path):
        reader, writer = await asyncio.open_unix_connection(socket_path)
        self._terminal = ShittyTerminal(reader, writer)

    async def get_shell(self):
        await self._terminal.hit_enter()
        while True:
            await self._terminal.drain()
            for l in self._terminal.scrollback:
                print("xx: %s" % l)
            self._terminal.clear_scrollback()
            if self._terminal.linebuffer.startswith("#"):
                print("shell")
                return ShittyShell(self._terminal)
            elif self._terminal.linebuffer.endswith("login:"):
                print("login prompt")
                self._console_socket.send("root\n".encode())
