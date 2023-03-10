import asyncio

from quumremote.terminal import ShittyTerminal


class ShittyShell:
    __slots__ = ["_terminal"]

    def __init__(self, terminal: ShittyTerminal):
        self._terminal = terminal

    async def dump_scrollback(self):
        await self._terminal.dump_scrollback()

    async def run(self, command: str):
        await self._terminal.send_line(command)
        # Get the return code
        await self._terminal.send_line("echo $?")
        return int(self._terminal.latest_line())

    async def run_detached(self, command: str):
        await self._terminal.send_line(command + "&")
