import asyncio
import socketio

async def send_message():
    sio = socketio.AsyncClient()

    @sio.event
    async def connect():
        print("Connection established")

    @sio.event
    async def connect_error(data):
        print("The connection failed!")

    @sio.event
    async def disconnect():
        print("Disconnected from server")

    @sio.on('message')
    async def on_message(msg):
        print(f"Server: {msg}")

    async def send_loop():
        while True:
            message = await asyncio.get_event_loop().run_in_executor(None, input, "Enter a message: ")
            await sio.send(message)

    await sio.connect('http://localhost:5000')
    await sio.start_background_task(send_loop)
    await sio.wait()

asyncio.run(send_message())
