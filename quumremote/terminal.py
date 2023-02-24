import asyncio
from asyncio import StreamReader, StreamWriter


class ShittyTerminal:
    __slots__ = ["_reader", "_writer", "scrollback", "linebuffer"]

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self.scrollback = []
        self.linebuffer = ""

    def clear_scrollback(self):
        self.scrollback = []

    def _append_to_linebuff(self, data: str):
        for char in data:
            if char == '\n':
                self.scrollback.append(self.linebuffer)
                self.linebuffer = ""
            elif char == '\r':
                pass
            else:
                self.linebuffer += char

    async def _poll(self):
        try:
            data = await asyncio.wait_for(self._reader.read(128), 1)
            decoded_data = data.decode()
            self._append_to_linebuff(decoded_data)
            return True
        except TimeoutError:
            return False

    async def drain(self):
        while True:
            if not await self._poll():
                break

    async def hit_enter(self):
        self._writer.write("\n".encode())
        await self._writer.drain()

    async def send_line(self, line):
        terminated_line = line + "\n"
        self._writer.write(terminated_line.encode())
        await self._writer.drain()
