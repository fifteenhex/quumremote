#!/usr/bin/env python3
import asyncio

from quumremote.managedquum import ManagedQUUM


async def main_loop():
    myquum = ManagedQUUM()
    await myquum.connect("/media/slimboy/coding/linuxgfxtester/testqemu_console")
    shell = await myquum.get_shell()

    await shell.run("killall chocolate-doom")
    await shell.dump_backtrace()

    await shell.run_detached("chocolate-doom")
    await asyncio.sleep(10)
    await shell.dump_backtrace()

    await shell.run("killall chocolate-doom")
    await shell.dump_backtrace()


if __name__ == '__main__':
    print("QUUMRemote")

    asyncio.run(main_loop())
