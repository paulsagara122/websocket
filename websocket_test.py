import asyncio
import websockets

async def test_websocket():
    uri = "ws://echo.websocket.org"  # Use a public echo server for testing
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello, WebSocket!")
        response = await websocket.recv()
        print(f"Received: {response}")

asyncio.run(test_websocket())
