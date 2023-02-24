#!/usr/bin/env python3
import asyncio

from quumremote.quum import ManagedQUUM
from quumremote.vnc import VNC2MPG


async def main_loop():
    myquum = ManagedQUUM()
    myvnc2mpg = VNC2MPG()

    await myquum.start()
    await asyncio.sleep(5)
    await myquum.connect()
    await myvnc2mpg.start_recording()

    shell = await myquum.get_shell()

    await shell.run("killall chocolate-doom")
    await shell.dump_scrollback()

    await shell.run_detached("chocolate-doom")
    await asyncio.sleep(10)
    await shell.dump_scrollback()

    await shell.run("killall chocolate-doom")
    await shell.dump_scrollback()

    await shell.run("poweroff")
    await shell.dump_scrollback()


if __name__ == '__main__':
    print("QUUMRemote")

    asyncio.run(main_loop())
