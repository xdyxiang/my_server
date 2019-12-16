#!/usr/bin/env python

# WS client example

import asyncio
import websockets

async def hello():
    async with websockets.connect(
            'ws://localhost:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


async def hlo():
    ws = websockets.connect('ws://localhost:8765')
    name = input("What's your name? ")
    await ws.send(name)
    print(f"> {name}")
    greeting = await ws.recv()
    print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hlo())
asyncio.get_event_loop().run_forever()
