"""
Finovate StreamX AI - Backend API
FastAPI REST API for remote control and web dashboard
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
from datetime import datetime

app = FastAPI(
    title="Finovate StreamX AI API",
    description="REST API for remote control and monitoring",
    version="1.0.0"
)

# CORS for web dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChannelModel(BaseModel):
    id: str
    name: str
    url: str
    category: str
    logo: Optional[str] = None

class PlaybackStatus(BaseModel):
    is_playing: bool
    channel_name: Optional[str] = None
    channel_url: Optional[str] = None
    position: float = 0.0
    duration: float = 0.0
    volume: int = 50
    muted: bool = False

class DVRRecording(BaseModel):
    id: str
    channel_name: str
    start_time: datetime
    end_time: datetime
    status: str  # recording, scheduled, completed
    file_path: Optional[str] = None

class SystemStatus(BaseModel):
    cpu_usage: float
    ram_usage: float
    network_speed: float
    active_streams: int
    recordings_count: int
    uptime: float

# Active connections for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Mock data (will be replaced with actual service calls)
current_playback: Optional[PlaybackStatus] = None
active_recordings: List[DVRRecording] = []

@app.get("/")
async def root():
    return {
        "name": "Finovate StreamX AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/playback",
            "/channels",
            "/recordings",
            "/system",
            "/ws/control"
        ]
    }

@app.get("/playback", response_model=PlaybackStatus)
async def get_playback_status():
    """Get current playback status"""
    if current_playback:
        return current_playback
    return PlaybackStatus(
        is_playing=False,
        volume=50,
        muted=False
    )

@app.post("/playback/play")
async def play_channel(channel_id: str, channel_url: str):
    """Start playing a channel"""
    global current_playback
    current_playback = PlaybackStatus(
        is_playing=True,
        channel_name=channel_id,
        channel_url=channel_url,
        position=0.0,
        volume=50
    )
    
    # Broadcast to all connected clients
    await manager.broadcast({
        "type": "playback_started",
        "channel": channel_id,
        "url": channel_url
    })
    
    return {"status": "playing", "channel": channel_id}

@app.post("/playback/pause")
async def pause_playback():
    """Pause current playback"""
    global current_playback
    if current_playback:
        current_playback.is_playing = False
    
    await manager.broadcast({"type": "playback_paused"})
    return {"status": "paused"}

@app.post("/playback/stop")
async def stop_playback():
    """Stop current playback"""
    global current_playback
    current_playback = None
    
    await manager.broadcast({"type": "playback_stopped"})
    return {"status": "stopped"}

@app.post("/playback/volume")
async def set_volume(volume: int):
    """Set volume (0-100)"""
    global current_playback
    if current_playback:
        current_playback.volume = max(0, min(100, volume))
    
    await manager.broadcast({"type": "volume_changed", "volume": volume})
    return {"status": "volume_set", "volume": volume}

@app.get("/channels")
async def get_channels(category: Optional[str] = None):
    """Get list of channels"""
    # This will integrate with IPTV service
    mock_channels = [
        {"id": "1", "name": "Sports HD", "category": "Sports", "url": "http://example.com/sports"},
        {"id": "2", "name": "Movies Plus", "category": "Movies", "url": "http://example.com/movies"},
        {"id": "3", "name": "News 24", "category": "News", "url": "http://example.com/news"},
    ]
    
    if category:
        mock_channels = [c for c in mock_channels if c["category"] == category]
    
    return {"channels": mock_channels, "count": len(mock_channels)}

@app.get("/recordings", response_model=List[DVRRecording])
async def get_recordings():
    """Get list of recordings"""
    return active_recordings

@app.post("/recordings/schedule")
async def schedule_recording(
    channel_id: str,
    start_time: datetime,
    end_time: datetime
):
    """Schedule a new recording"""
    recording = DVRRecording(
        id=f"rec_{datetime.now().timestamp()}",
        channel_name=channel_id,
        start_time=start_time,
        end_time=end_time,
        status="scheduled"
    )
    active_recordings.append(recording)
    
    await manager.broadcast({
        "type": "recording_scheduled",
        "recording": recording.dict()
    })
    
    return {"status": "scheduled", "recording_id": recording.id}

@app.delete("/recordings/{recording_id}")
async def cancel_recording(recording_id: str):
    """Cancel a scheduled recording"""
    global active_recordings
    active_recordings = [r for r in active_recordings if r.id != recording_id]
    
    await manager.broadcast({
        "type": "recording_cancelled",
        "recording_id": recording_id
    })
    
    return {"status": "cancelled"}

@app.get("/system", response_model=SystemStatus)
async def get_system_status():
    """Get system status and metrics"""
    return SystemStatus(
        cpu_usage=25.5,
        ram_usage=312.0,
        network_speed=15.2,
        active_streams=1 if current_playback and current_playback.is_playing else 0,
        recordings_count=len([r for r in active_recordings if r.status == "recording"]),
        uptime=3600.0
    )

@app.websocket("/ws/control")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time control"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle control commands
            if message.get("type") == "play":
                await play_channel(
                    message.get("channel_id", ""),
                    message.get("channel_url", "")
                )
            elif message.get("type") == "pause":
                await pause_playback()
            elif message.get("type") == "stop":
                await stop_playback()
            elif message.get("type") == "volume":
                await set_volume(message.get("volume", 50))
            
            # Echo confirmation
            await websocket.send_json({
                "status": "command_received",
                "command": message.get("type")
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({"type": "client_disconnected"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
