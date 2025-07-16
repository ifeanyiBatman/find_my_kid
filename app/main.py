from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import asyncio
import httpx

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def read_root(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return templates.TemplateResponse("dashboard.html", {"request": {}})

# WebSocket endpoint for GPS updates
@app.websocket("/ws/gps")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast GPS data to all connected clients
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Video proxy endpoint
@app.get("/proxy/video")
async def proxy_video(request: Request):
    camera_url = request.query_params.get("url")
    if not camera_url:
        raise HTTPException(status_code=400, detail="Missing camera URL parameter")
    
    # Basic URL validation
    if not camera_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL protocol")
    
    async with httpx.AsyncClient() as client:
        try:
            print(f"Proxying video from: {camera_url}")
            response = await client.get(camera_url, timeout=10.0)
            if response.status_code != 200:
                print(f"Camera server error: {response.status_code}")
                raise HTTPException(status_code=response.status_code, detail="Camera server error")
            
            content_type = response.headers.get("Content-Type", "multipart/x-mixed-replace")
            print(f"Received Content-Type: {content_type}")
            
            # Set proper headers for MJPEG stream
            return StreamingResponse(
                response.aiter_bytes(),
                media_type='multipart/x-mixed-replace; boundary=--myboundary',
                headers={
                    "Cache-Control": "no-cache, no-store, must-revalidate",
                    "Connection": "close",
                    "Content-Type": "multipart/x-mixed-replace; boundary=--myboundary"
                }
            )
        except httpx.RequestError as e:
            print(f"Proxy connection error: {str(e)}")
            raise HTTPException(status_code=503, detail="Could not connect to camera")