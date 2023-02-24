import asyncio


class VNC2MPG:
    async def start_recording(self):
        await asyncio.create_subprocess_shell("/media/slimboy/coding/linuxgfxtester/vnc2mpg -o vncrecording.mp4")
