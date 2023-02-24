#!/usr/bin/env python3
import asyncio

from quumremote.quum import ManagedQUUM
from quumremote.vnc import VNC2MPG


async def test_chocodoom(shell):
    await shell.run("killall chocolate-doom")
    await shell.dump_scrollback()

    await shell.run_detached("chocolate-doom")
    await asyncio.sleep(30)
    await shell.dump_scrollback()

    await shell.run("killall chocolate-doom")
    await shell.dump_scrollback()


async def test_scumm(shell):
    await shell.run("killall scummvm")
    await shell.dump_scrollback()

    await shell.run_detached("scummvm")
    await asyncio.sleep(30)
    await shell.dump_scrollback()

    await shell.run("killall scummvm")
    await shell.dump_scrollback()


async def main_loop():
    myquum = ManagedQUUM()
    myvnc2mpg = VNC2MPG()

    await myquum.start()
    await asyncio.sleep(20)
    await myquum.connect()
    await myvnc2mpg.start_recording()

    shell = await myquum.get_shell()
    await test_chocodoom(shell)

    await shell.run("poweroff")
    await shell.dump_scrollback()


if __name__ == '__main__':
    print("QUUMRemote")

    asyncio.run(main_loop())
