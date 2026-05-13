"""
Finovate StreamX AI - Web Dashboard Frontend
HTML/CSS/JS dashboard for remote control
"""

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Finovate StreamX AI - Remote Dashboard</title>
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

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

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

        .status-label {
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .status-value {
            font-weight: bold;
            color: var(--accent);
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }

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
            box-shadow: 0 12px 40px rgba(0, 229, 255, 0.15);
        }

        .card h2 {
            color: var(--accent);
            margin-bottom: 20px;
            font-size: 1.5em;
        }

        .control-btn {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, var(--primary), #1565C0);
            color: white;
        }

        .control-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4);
        }

        .control-btn.danger {
            background: linear-gradient(135deg, var(--danger), #C62828);
        }

        .control-btn.success {
            background: linear-gradient(135deg, var(--success), #00897B);
        }

        .volume-slider {
            width: 100%;
            margin: 15px 0;
            -webkit-appearance: none;
            height: 10px;
            border-radius: 5px;
            background: var(--bg-primary);
            outline: none;
        }

        .volume-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            background: var(--accent);
            cursor: pointer;
            box-shadow: 0 0 10px var(--accent);
        }

        .channel-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .channel-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background: rgba(30, 136, 229, 0.1);
            border-radius: 10px;
            border: 1px solid rgba(30, 136, 229, 0.2);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .channel-item:hover {
            background: rgba(30, 136, 229, 0.2);
            border-color: var(--accent);
            transform: translateX(5px);
        }

        .channel-item.active {
            border-color: var(--success);
            background: rgba(0, 255, 198, 0.1);
        }

        .channel-logo {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            margin-right: 15px;
            background: var(--bg-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
        }

        .channel-info {
            flex: 1;
        }

        .channel-name {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .channel-category {
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        .recording-item {
            padding: 15px;
            margin: 10px 0;
            background: rgba(255, 82, 82, 0.1);
            border-radius: 10px;
            border-left: 4px solid var(--danger);
        }

        .recording-item.scheduled {
            border-left-color: var(--accent);
            background: rgba(0, 229, 255, 0.1);
        }

        .recording-item.completed {
            border-left-color: var(--success);
            background: rgba(0, 255, 198, 0.1);
        }

        .player-preview {
            width: 100%;
            aspect-ratio: 16/9;
            background: var(--bg-primary);
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--primary);
        }

        .player-placeholder {
            color: var(--text-secondary);
            font-size: 1.2em;
        }

        .connection-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            z-index: 1000;
        }

        .connected {
            background: var(--success);
            color: #000;
        }

        .disconnected {
            background: var(--danger);
            color: white;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .loading {
            animation: pulse 1.5s infinite;
        }

        /* Mobile responsive */
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 1.5em;
            }
            
            .status-bar {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Finovate StreamX AI</h1>
        <p style="color: var(--text-secondary);">Remote Dashboard & Control Center</p>
        <div class="status-bar" id="statusBar">
            <div class="status-item">
                <div class="status-label">Status</div>
                <div class="status-value" id="systemStatus">Connecting...</div>
            </div>
            <div class="status-item">
                <div class="status-label">CPU Usage</div>
                <div class="status-value" id="cpuUsage">--%</div>
            </div>
            <div class="status-item">
                <div class="status-label">RAM Usage</div>
                <div class="status-value" id="ramUsage">-- MB</div>
            </div>
            <div class="status-item">
                <div class="status-label">Active Streams</div>
                <div class="status-value" id="activeStreams">0</div>
            </div>
        </div>
    </div>

    <div class="container">
        <!-- Player Control Card -->
        <div class="card">
            <h2>📺 Player Control</h2>
            <div class="player-preview" id="playerPreview">
                <div class="player-placeholder">No channel playing</div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <button class="control-btn success" onclick="playChannel()">▶ Play</button>
                <button class="control-btn" onclick="pausePlayback()">⏸ Pause</button>
                <button class="control-btn danger" onclick="stopPlayback()">⏹ Stop</button>
                <button class="control-btn" onclick="toggleMute()">🔊 Mute</button>
            </div>
            <div style="margin-top: 20px;">
                <label style="color: var(--text-secondary);">Volume: <span id="volumeValue">50</span>%</label>
                <input type="range" class="volume-slider" id="volumeSlider" 
                       min="0" max="100" value="50" oninput="changeVolume(this.value)">
            </div>
        </div>

        <!-- Channels Card -->
        <div class="card">
            <h2>📡 Live Channels</h2>
            <div class="channel-list" id="channelList">
                <div class="loading">Loading channels...</div>
            </div>
        </div>

        <!-- Recordings Card -->
        <div class="card">
            <h2>🎬 DVR Recordings</h2>
            <div id="recordingsList">
                <div class="loading">Loading recordings...</div>
            </div>
            <button class="control-btn" style="margin-top: 15px;" onclick="showScheduleDialog()">
                📅 Schedule Recording
            </button>
        </div>

        <!-- System Info Card -->
        <div class="card">
            <h2>💻 System Information</h2>
            <div id="systemInfo">
                <div class="status-item" style="margin: 10px 0;">
                    <div class="status-label">Network Speed</div>
                    <div class="status-value" id="networkSpeed">-- Mbps</div>
                </div>
                <div class="status-item" style="margin: 10px 0;">
                    <div class="status-label">Recordings Count</div>
                    <div class="status-value" id="recordingsCount">0</div>
                </div>
                <div class="status-item" style="margin: 10px 0;">
                    <div class="status-label">Uptime</div>
                    <div class="status-value" id="uptime">--</div>
                </div>
            </div>
        </div>
    </div>

    <div class="connection-status disconnected" id="connectionStatus">
        Disconnected
    </div>

    <script>
        const API_BASE = 'http://localhost:8000';
        let ws = null;
        let currentChannel = null;

        // WebSocket connection
        function connectWebSocket() {
            const wsUrl = `ws://localhost:8000/ws/control`;
            ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                updateConnectionStatus(true);
                console.log('Connected to StreamX AI');
            };

            ws.onclose = () => {
                updateConnectionStatus(false);
                setTimeout(connectWebSocket, 3000); // Reconnect
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };
        }

        function updateConnectionStatus(connected) {
            const statusEl = document.getElementById('connectionStatus');
            if (connected) {
                statusEl.textContent = 'Connected ✓';
                statusEl.className = 'connection-status connected';
            } else {
                statusEl.textContent = 'Disconnected';
                statusEl.className = 'connection-status disconnected';
            }
        }

        function handleWebSocketMessage(data) {
            console.log('Received:', data);
            if (data.type === 'playback_started') {
                updatePlayerPreview(data.channel);
            }
        }

        // API calls
        async function fetchSystemStatus() {
            try {
                const response = await fetch(`${API_BASE}/system`);
                const data = await response.json();
                
                document.getElementById('cpuUsage').textContent = data.cpu_usage.toFixed(1) + '%';
                document.getElementById('ramUsage').textContent = data.ram_usage.toFixed(0) + ' MB';
                document.getElementById('activeStreams').textContent = data.active_streams;
                document.getElementById('networkSpeed').textContent = data.network_speed.toFixed(1) + ' Mbps';
                document.getElementById('recordingsCount').textContent = data.recordings_count;
                document.getElementById('uptime').textContent = formatUptime(data.uptime);
                document.getElementById('systemStatus').textContent = 'Online';
            } catch (error) {
                console.error('Error fetching system status:', error);
                document.getElementById('systemStatus').textContent = 'Offline';
            }
        }

        async function fetchChannels() {
            try {
                const response = await fetch(`${API_BASE}/channels`);
                const data = await response.json();
                
                const channelList = document.getElementById('channelList');
                channelList.innerHTML = '';
                
                data.channels.forEach(channel => {
                    const item = createChannelItem(channel);
                    channelList.appendChild(item);
                });
            } catch (error) {
                console.error('Error fetching channels:', error);
            }
        }

        async function fetchRecordings() {
            try {
                const response = await fetch(`${API_BASE}/recordings`);
                const data = await response.json();
                
                const recordingsList = document.getElementById('recordingsList');
                recordingsList.innerHTML = '';
                
                if (data.length === 0) {
                    recordingsList.innerHTML = '<p style="color: var(--text-secondary);">No recordings</p>';
                    return;
                }
                
                data.forEach(rec => {
                    const item = createRecordingItem(rec);
                    recordingsList.appendChild(item);
                });
            } catch (error) {
                console.error('Error fetching recordings:', error);
            }
        }

        function createChannelItem(channel) {
            const div = document.createElement('div');
            div.className = 'channel-item';
            div.onclick = () => selectChannel(channel);
            
            div.innerHTML = `
                <div class="channel-logo">📺</div>
                <div class="channel-info">
                    <div class="channel-name">${channel.name}</div>
                    <div class="channel-category">${channel.category}</div>
                </div>
            `;
            
            return div;
        }

        function createRecordingItem(recording) {
            const div = document.createElement('div');
            div.className = `recording-item ${recording.status}`;
            
            div.innerHTML = `
                <div class="channel-name">${recording.channel_name}</div>
                <div class="channel-category">
                    ${recording.start_time} - ${recording.end_time}<br>
                    Status: ${recording.status}
                </div>
            `;
            
            return div;
        }

        function selectChannel(channel) {
            currentChannel = channel;
            
            // Update UI
            document.querySelectorAll('.channel-item').forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
            
            updatePlayerPreview(channel.name);
        }

        function updatePlayerPreview(channelName) {
            const preview = document.getElementById('playerPreview');
            preview.innerHTML = `
                <div style="text-align: center;">
                    <div style="font-size: 3em; margin-bottom: 10px;">📺</div>
                    <div style="color: var(--accent); font-weight: bold;">${channelName}</div>
                    <div style="color: var(--success);">Now Playing</div>
                </div>
            `;
        }

        // Control functions
        function playChannel() {
            if (!currentChannel) {
                alert('Please select a channel first');
                return;
            }
            
            sendCommand('play', {
                channel_id: currentChannel.id,
                channel_url: currentChannel.url
            });
        }

        function pausePlayback() {
            sendCommand('pause', {});
        }

        function stopPlayback() {
            sendCommand('stop', {});
        }

        function toggleMute() {
            // Implement mute toggle
            alert('Mute toggled');
        }

        function changeVolume(value) {
            document.getElementById('volumeValue').textContent = value;
            sendCommand('volume', { volume: parseInt(value) });
        }

        function sendCommand(type, data) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: type,
                    ...data
                }));
            } else {
                alert('Not connected to server');
            }
        }

        function showScheduleDialog() {
            alert('Schedule recording dialog (to be implemented)');
        }

        function formatUptime(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            return `${hours}h ${minutes}m`;
        }

        // Initialize
        window.onload = () => {
            connectWebSocket();
            fetchSystemStatus();
            fetchChannels();
            fetchRecordings();
            
            // Refresh every 5 seconds
            setInterval(fetchSystemStatus, 5000);
            setInterval(fetchChannels, 30000);
            setInterval(fetchRecordings, 10000);
        };
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    # Save dashboard to file
    with open("web_dashboard/index.html", "w", encoding="utf-8") as f:
        f.write(DASHBOARD_HTML)
    print("Dashboard saved to web_dashboard/index.html")
