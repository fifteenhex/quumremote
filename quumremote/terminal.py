import asyncio
from asyncio import StreamReader, StreamWriter


class ShittyTerminal:
    __slots__ = ["_reader", "_writer", "scrollback", "linebuffer"]

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self._reader = reader
        self._writer = writer
        self.scrollback = []
        self.linebuffer = ""

    async def dump_scrollback(self):
        for line in self.scrollback:
            print(">>> %s" % line)
        self.clear_scrollback()

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
        while True:
            try:
                data = await asyncio.wait_for(self._reader.read(128), 1)
                decoded_data = data.decode()
                self._append_to_linebuff(decoded_data)
            except TimeoutError:
                break

    async def send_line(self, line: str):
        terminated_line = line + "\n"
        self._writer.write(terminated_line.encode())
        await asyncio.gather(self._writer.drain(), self._poll())

    async def hit_enter(self):
        await self.send_line("")

    def latest_line(self):
        return self.scrollback[-1]
