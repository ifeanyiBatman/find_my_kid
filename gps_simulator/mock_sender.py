import asyncio
import websockets
import random
import json

async def send_gps_data():
    uri = "ws://localhost:8000/ws/gps"
    async with websockets.connect(uri) as websocket:
        while True:
            # Simulate GPS coordinates in Lagos
            lat = 6.3754 + random.uniform(-0.01, 0.01)
            lng = 7.5209 + random.uniform(-0.01, 0.01)
            data = json.dumps({"lat": lat, "lng": lng})
            await websocket.send(data)
            print(f"Sent: {data}")
            await asyncio.sleep(5)  # Send every 5 seconds

if __name__ == "__main__":
    asyncio.run(send_gps_data())
