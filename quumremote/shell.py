from quumremote.terminal import ShittyTerminal


class ShittyShell:
    __slots__ = ["_terminal"]

    def __init__(self, terminal: ShittyTerminal):
        self._terminal = terminal

    async def run(self, command: str):
        await self._terminal.send_line(command)
        await self._terminal.drain()

    async def run_detached(self, command: str):
        await self._terminal.send_line(command + "&")
        await self._terminal.drain()

    async def dump_backtrace(self):
        await self._terminal.drain()
        for line in self._terminal.scrollback:
            print(">>> %s" % line)
        self._terminal.clear_scrollback()
