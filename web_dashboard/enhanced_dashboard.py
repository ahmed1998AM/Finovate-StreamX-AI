"""
Finovate StreamX AI - Enhanced Web Dashboard
Complete Flask-based web interface with real-time control
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
Contact: 01225155329 | gogom8870@gmail.com
"""

import os
import sys
import asyncio
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import logging

from flask import Flask, render_template_string, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

logger = logging.getLogger(__name__)


class WebDashboardServer:
    """Enhanced Web Dashboard Server with real-time updates"""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 5000):
        self.host = host
        self.port = port
        
        # Flask app
        self.app = Flask(__name__)
        self.app.secret_key = 'streamx_secret_key_2024'
        CORS(self.app)
        
        # Socket.IO for real-time updates
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # State
        self.integration_controller = None
        self.connected_clients = 0
        
        # Setup routes
        self._setup_routes()
        self._setup_socket_events()
        
        logger.info(f"Web Dashboard Server initialized on {host}:{port}")
    
    def set_integration_controller(self, controller):
        """Set integration controller for API access"""
        self.integration_controller = controller
        logger.info("Integration controller connected to web dashboard")
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Serve main dashboard"""
            return render_template_string(DASHBOARD_HTML)
        
        @self.app.route('/api/status')
        def get_status():
            """Get system status"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'})
            
            return jsonify({
                'playback': self.integration_controller.get_playback_status(),
                'recording': self.integration_controller.get_recording_status(),
                'channels_loaded': len(self.integration_controller.loaded_channels),
                'favorites': len(self.integration_controller.favorite_channels),
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/channels')
        def get_channels():
            """Get all channels"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'})
            
            category = request.args.get('category', 'all')
            country = request.args.get('country', 'all')
            
            channels = self.integration_controller.loaded_channels
            
            if category != 'all':
                channels = [ch for ch in channels if ch.get('category') == category]
            
            if country != 'all':
                channels = [ch for ch in channels if ch.get('country') == country]
            
            return jsonify({'channels': channels, 'count': len(channels)})
        
        @self.app.route('/api/play', methods=['POST'])
        def play_channel():
            """Play a channel"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'}), 400
            
            data = request.json
            channel_name = data.get('channel')
            
            if not channel_name:
                return jsonify({'error': 'Channel name required'}), 400
            
            # Find channel
            channel = next(
                (ch for ch in self.integration_controller.loaded_channels 
                 if ch.get('name') == channel_name), 
                None
            )
            
            if not channel:
                return jsonify({'error': 'Channel not found'}), 404
            
            success = self.integration_controller.play_channel(channel)
            
            if success:
                self.socketio.emit('playback_started', {'channel': channel_name})
                return jsonify({'success': True, 'message': f'Playing {channel_name}'})
            else:
                return jsonify({'success': False, 'error': 'Failed to play'}), 500
        
        @self.app.route('/api/record', methods=['POST'])
        def toggle_recording():
            """Toggle recording"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'}), 400
            
            success = self.integration_controller.toggle_recording()
            status = self.integration_controller.get_recording_status()
            
            return jsonify({
                'success': success,
                'recording': status
            })
        
        @self.app.route('/api/favorites', methods=['GET'])
        def get_favorites():
            """Get favorite channels"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'})
            
            favorites = self.integration_controller.get_favorites()
            return jsonify({'favorites': favorites, 'count': len(favorites)})
        
        @self.app.route('/api/favorites', methods=['POST'])
        def add_favorite():
            """Add channel to favorites"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'}), 400
            
            data = request.json
            channel_name = data.get('channel')
            
            if not channel_name:
                return jsonify({'error': 'Channel name required'}), 400
            
            success = self.integration_controller.add_to_favorites(channel_name)
            return jsonify({'success': success})
        
        @self.app.route('/api/search')
        def search_channels():
            """Search channels"""
            if not self.integration_controller:
                return jsonify({'error': 'Controller not connected'})
            
            query = request.args.get('q', '')
            results = self.integration_controller.search_channels(query)
            
            return jsonify({'results': results, 'count': len(results)})
        
        @self.app.route('/api/dvr/recordings')
        def get_recordings():
            """Get DVR recordings"""
            if not self.integration_controller or not self.integration_controller.dvr_manager:
                return jsonify({'error': 'DVR not available'})
            
            recordings = self.integration_controller.dvr_manager.get_recordings()
            return jsonify({
                'recordings': [
                    {
                        'id': r.id,
                        'channel': r.channel_name,
                        'start': r.start_time,
                        'end': r.end_time,
                        'duration': r.duration_seconds,
                        'status': r.status,
                        'size_mb': r.size_mb
                    }
                    for r in recordings
                ]
            })
        
        @self.app.route('/api/system/info')
        def get_system_info():
            """Get system information"""
            return jsonify({
                'name': 'Finovate StreamX AI',
                'version': '1.0.0',
                'developer': 'Ahmed Mostafa Ibrahim | Finovate – AHMED EG',
                'contact': '01225155329 | gogom8870@gmail.com',
                'features': [
                    'IPTV Streaming',
                    'DVR Recording',
                    'AI Assistant',
                    'Multi-Language',
                    'Cloud Sync',
                    'Torrent Streaming',
                    'Plugin System'
                ],
                'stats': {
                    'connected_clients': self.connected_clients,
                    'uptime': str(datetime.now())
                }
            })
    
    def _setup_socket_events(self):
        """Setup Socket.IO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            self.connected_clients += 1
            emit('connected', {'clients': self.connected_clients})
            logger.info(f"Client connected. Total: {self.connected_clients}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.connected_clients -= 1
            emit('disconnected', {'clients': self.connected_clients})
            logger.info(f"Client disconnected. Total: {self.connected_clients}")
        
        @self.socketio.on('request_status')
        def handle_status_request():
            if self.integration_controller:
                status = {
                    'playback': self.integration_controller.get_playback_status(),
                    'recording': self.integration_controller.get_recording_status()
                }
                emit('status_update', status)
    
    def broadcast_playback_update(self, data: dict):
        """Broadcast playback update to all clients"""
        self.socketio.emit('playback_update', data)
    
    def broadcast_recording_update(self, data: dict):
        """Broadcast recording update to all clients"""
        self.socketio.emit('recording_update', data)
    
    def run(self, debug: bool = False):
        """Start the web server"""
        logger.info(f"Starting Web Dashboard on http://{self.host}:{self.port}")
        self.socketio.run(self.app, host=self.host, port=self.port, debug=debug)


# Complete HTML Dashboard
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finovate StreamX AI - Remote Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        :root {
            --bg-primary: #0B1020;
            --bg-card: #121A2B;
            --primary: #1E88E5;
            --accent: #00E5FF;
            --success: #00FFC6;
            --danger: #FF5252;
            --text-primary: #FFFFFF;
            --text-secondary: #B0BEC5;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }

        .header {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-primary));
            padding: 20px;
            border-bottom: 2px solid var(--accent);
            box-shadow: 0 4px 20px rgba(0, 229, 255, 0.2);
        }

        .header h1 {
            font-size: 2em;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .status-bar {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }

        .status-item {
            background: rgba(30, 136, 229, 0.1);
            padding: 10px 20px;
            border-radius: 10px;
            border: 1px solid var(--primary);
            backdrop-filter: blur(10px);
        }

        .status-label { color: var(--text-secondary); font-size: 0.9em; }
        .status-value { font-weight: bold; color: var(--accent); }

        .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: var(--bg-card);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(30, 136, 229, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: var(--accent);
        }

        .card h2 {
            color: var(--accent);
            margin-bottom: 15px;
            font-size: 1.3em;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 14px;
            transition: all 0.3s ease;
            margin: 5px;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
        }

        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0, 229, 255, 0.4);
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-success {
            background: var(--success);
            color: #000;
        }

        .channel-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .channel-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            margin: 8px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .channel-item:hover {
            background: rgba(30, 136, 229, 0.2);
            transform: translateX(5px);
        }

        .channel-name { font-weight: bold; }
        .channel-info { color: var(--text-secondary); font-size: 0.85em; }

        .control-panel {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }

        .search-box {
            width: 100%;
            padding: 12px;
            border: 1px solid rgba(30, 136, 229, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            font-size: 14px;
            margin-bottom: 15px;
        }

        .search-box:focus {
            outline: none;
            border-color: var(--accent);
        }

        .indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .indicator.live { background: var(--danger); animation: pulse 1s infinite; }
        .indicator.recording { background: var(--success); animation: pulse 1s infinite; }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📺 Finovate StreamX AI</h1>
        <p style="color: var(--text-secondary); margin-bottom: 15px;">
            Remote Dashboard Control Panel
        </p>
        <div class="status-bar">
            <div class="status-item">
                <div class="status-label">Connection Status</div>
                <div class="status-value" id="connectionStatus">Connecting...</div>
            </div>
            <div class="status-item">
                <div class="status-label">Connected Clients</div>
                <div class="status-value" id="clientCount">0</div>
            </div>
            <div class="status-item">
                <div class="status-label">Current Channel</div>
                <div class="status-value" id="currentChannel">None</div>
            </div>
            <div class="status-item">
                <div class="status-label">Recording Status</div>
                <div class="status-value" id="recordingStatus">Inactive</div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="grid">
            <!-- Playback Control -->
            <div class="card">
                <h2>▶️ Playback Control</h2>
                <div id="nowPlaying" style="margin-bottom: 15px; color: var(--text-secondary);">
                    No channel playing
                </div>
                <div class="control-panel">
                    <button class="btn btn-primary" onclick="refreshStatus()">🔄 Refresh</button>
                    <button class="btn btn-danger" onclick="stopPlayback()">⏹ Stop</button>
                </div>
            </div>

            <!-- DVR Control -->
            <div class="card">
                <h2>📼 DVR Recording</h2>
                <div id="recordingInfo" style="margin-bottom: 15px; color: var(--text-secondary);">
                    No active recordings
                </div>
                <div class="control-panel">
                    <button class="btn btn-success" onclick="toggleRecording()">⏺ Toggle Record</button>
                    <button class="btn btn-primary" onclick="viewRecordings()">📋 View Recordings</button>
                </div>
            </div>

            <!-- Channels -->
            <div class="card" style="grid-column: span 2;">
                <h2>📺 Channel List</h2>
                <input type="text" class="search-box" id="searchBox" 
                       placeholder="🔍 Search channels..." onkeyup="searchChannels()">
                <div class="channel-list" id="channelList">
                    Loading channels...
                </div>
            </div>
        </div>

        <!-- System Info -->
        <div class="card">
            <h2>ℹ️ System Information</h2>
            <div id="systemInfo">Loading...</div>
        </div>
    </div>

    <div class="footer">
        <p>Finovate StreamX AI v1.0.0 | Developer: Ahmed Mostafa Ibrahim</p>
        <p>Contact: 01225155329 | gogom8870@gmail.com</p>
    </div>

    <script>
        // Socket.IO connection
        const socket = io();

        socket.on('connect', () => {
            document.getElementById('connectionStatus').textContent = '✅ Connected';
            document.getElementById('connectionStatus').style.color = '#00FFC6';
            refreshStatus();
        });

        socket.on('disconnect', () => {
            document.getElementById('connectionStatus').textContent = '❌ Disconnected';
            document.getElementById('connectionStatus').style.color = '#FF5252';
        });

        socket.on('status_update', (data) => {
            updateStatus(data);
        });

        socket.on('playback_update', (data) => {
            if (data.channel) {
                document.getElementById('currentChannel').textContent = data.channel;
            }
        });

        // Fetch functions
        async function refreshStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateStatus(data);
            } catch (error) {
                console.error('Failed to fetch status:', error);
            }
        }

        function updateStatus(data) {
            if (data.playback && data.playback.channel) {
                document.getElementById('currentChannel').textContent = data.playback.channel.name || 'Unknown';
                document.getElementById('nowPlaying').innerHTML = 
                    `<strong>Now Playing:</strong> ${data.playback.channel.name}<br>
                     Volume: ${data.playback.volume || 80}%`;
            }

            if (data.recording && data.recording.active) {
                document.getElementById('recordingStatus').textContent = '🔴 Recording';
                document.getElementById('recordingStatus').style.color = '#FF5252';
                document.getElementById('recordingInfo').textContent = 
                    `Active: ${data.recording.count} recording(s)`;
            } else {
                document.getElementById('recordingStatus').textContent = 'Inactive';
                document.getElementById('recordingStatus').style.color = '#B0BEC5';
            }

            if (data.channels_loaded !== undefined) {
                loadChannels();
            }
        }

        async function loadChannels() {
            try {
                const response = await fetch('/api/channels');
                const data = await response.json();
                renderChannelList(data.channels);
            } catch (error) {
                console.error('Failed to load channels:', error);
            }
        }

        function renderChannelList(channels) {
            const list = document.getElementById('channelList');
            
            if (!channels || channels.length === 0) {
                list.innerHTML = '<p style="color: var(--text-secondary);">No channels available</p>';
                return;
            }

            list.innerHTML = channels.slice(0, 50).map(ch => `
                <div class="channel-item">
                    <div>
                        <div class="channel-name">${ch.name || 'Unknown'}</div>
                        <div class="channel-info">${ch.category || 'General'} | ${ch.country || 'Unknown'}</div>
                    </div>
                    <button class="btn btn-primary" onclick="playChannel('${ch.name}')">▶ Play</button>
                </div>
            `).join('');
        }

        async function playChannel(channelName) {
            try {
                const response = await fetch('/api/play', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({channel: channelName})
                });
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('currentChannel').textContent = channelName;
                } else {
                    alert('Failed to play channel: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                console.error('Failed to play channel:', error);
            }
        }

        async function toggleRecording() {
            try {
                const response = await fetch('/api/record', {method: 'POST'});
                const data = await response.json();
                
                if (data.success) {
                    refreshStatus();
                }
            } catch (error) {
                console.error('Failed to toggle recording:', error);
            }
        }

        async function stopPlayback() {
            alert('Stop functionality will be implemented soon');
        }

        async function viewRecordings() {
            try {
                const response = await fetch('/api/dvr/recordings');
                const data = await response.json();
                
                if (data.recordings && data.recordings.length > 0) {
                    alert('Recordings:\\n' + data.recordings.map(r => 
                        `${r.channel} - ${new Date(r.start).toLocaleString()}`
                    ).join('\\n'));
                } else {
                    alert('No recordings found');
                }
            } catch (error) {
                console.error('Failed to fetch recordings:', error);
            }
        }

        async function searchChannels() {
            const query = document.getElementById('searchBox').value;
            
            if (query.length < 2) {
                loadChannels();
                return;
            }

            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                renderChannelList(data.results);
            } catch (error) {
                console.error('Failed to search channels:', error);
            }
        }

        // Load system info
        async function loadSystemInfo() {
            try {
                const response = await fetch('/api/system/info');
                const data = await response.json();
                
                document.getElementById('systemInfo').innerHTML = `
                    <p><strong>Name:</strong> ${data.name}</p>
                    <p><strong>Version:</strong> ${data.version}</p>
                    <p><strong>Developer:</strong> ${data.developer}</p>
                    <p><strong>Features:</strong> ${data.features.join(', ')}</p>
                    <p><strong>Connected Clients:</strong> ${data.stats.connected_clients}</p>
                `;
            } catch (error) {
                console.error('Failed to load system info:', error);
            }
        }

        // Initialize
        loadChannels();
        loadSystemInfo();

        // Auto-refresh every 10 seconds
        setInterval(refreshStatus, 10000);
    </script>
</body>
</html>
'''


# Test function
if __name__ == "__main__":
    server = WebDashboardServer(host='0.0.0.0', port=5000)
    print("🌐 Starting Web Dashboard...")
    print("📡 Access at: http://localhost:5000")
    server.run(debug=True)
