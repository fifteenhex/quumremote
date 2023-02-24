import socket
import asyncio

from quumremote.terminal import ShittyTerminal
from quumremote.shell import ShittyShell


class ManagedQUUM:
    __slots__ = ['_terminal', '_shell', '_console_socket_path']

    def __init__(self):
        self._terminal = None

    async def start(self):
        self._console_socket_path = "/media/slimboy/coding/linuxgfxtester/testqemu_console"
        await asyncio.create_subprocess_shell(
            "/media/slimboy/coding/linuxgfxtester/buildroot/output/host/bin/qemu-system-x86_64 " +
            "-machine q35 " +
            "-m 1G " +
            "-vga virtio " +
            "-device virtio-serial,max_ports=1 " +
            "-chardev socket,id=testqemu_console,path=%s,server=yes,wait=no " % (self._console_socket_path) +
            "-device virtconsole,chardev=testqemu_console,name=test_console " +
            "-kernel /media/slimboy/coding/linuxgfxtester/buildroot/output/images/bzImage " +
            "-append \"quiet\""
        )

    async def connect(self):
        reader, writer = await asyncio.open_unix_connection(self._console_socket_path)
        self._terminal = ShittyTerminal(reader, writer)

    async def get_shell(self):
        while True:
            await self._terminal.hit_enter()
            if self._terminal.linebuffer.startswith("#"):
                print("Got shell...")
                return ShittyShell(self._terminal)
            elif self._terminal.linebuffer.endswith("login: "):
                print("Got login prompt...")
                await self._terminal.send_line("root")
            else:
                print("Trying to work out VM state...")
                print("linebuffer: \"%s\"" % self._terminal.linebuffer)
                await self._terminal.dump_scrollback()
