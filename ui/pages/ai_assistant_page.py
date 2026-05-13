"""
AI Assistant Page Module
=========================
AI chat interface with voice commands and smart recommendations.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QTextEdit, QPushButton, QScrollArea,
    QListWidget, QListWidgetItem, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AIAssistantPage(QWidget):
    """AI Assistant page with chat interface."""
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the AI Assistant page UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Left panel - AI Agents
        agents_panel = self._create_agents_panel()
        main_layout.addWidget(agents_panel, 1)
        
        # Right panel - Chat interface
        chat_panel = self._create_chat_interface()
        main_layout.addWidget(chat_panel, 3)
    
    def _create_agents_panel(self) -> QFrame:
        """Create AI agents selection panel."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        
        layout = QVBoxLayout(frame)
        
        title = QLabel("🤖 AI Agents")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Agent list
        self.agent_list = QListWidget()
        self.agent_list.setObjectName("agentList")
        
        agents = [
            ("💬 General Assistant", "Chat & questions"),
            ("🔧 IPTV Repair Agent", "Fix broken streams"),
            ("📋 Playlist Agent", "Manage playlists"),
            ("📺 EPG Agent", "Electronic program guide"),
            ("📝 Subtitle Agent", "Auto subtitles"),
            ("⚡ Automation Agent", "Auto tasks"),
            ("👨‍💻 Developer Agent", "Code help"),
        ]
        
        for agent_name, agent_desc in agents:
            item = QListWidgetItem(f"{agent_name}\n{agent_desc}")
            item.setFont(QFont("Segoe UI", 10))
            self.agent_list.addItem(item)
        
        layout.addWidget(self.agent_list)
        
        # Provider selection
        provider_label = QLabel("AI Provider:")
        provider_label.setObjectName("secondaryLabel")
        layout.addWidget(provider_label)
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "OpenAI", "Gemini", "Claude", "DeepSeek", 
            "Grok", "OpenRouter", "Ollama", "LM Studio"
        ])
        layout.addWidget(self.provider_combo)
        
        return frame
    
    def _create_chat_interface(self) -> QFrame:
        """Create chat interface."""
        frame = QFrame()
        frame.setObjectName("glassFrame")
        
        layout = QVBoxLayout(frame)
        
        # Chat header
        header = QLabel("💬 AI Chat Assistant")
        header.setObjectName("titleLabel")
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # Chat messages area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setObjectName("chatScroll")
        
        self.chat_container = QFrame()
        self.chat_container.setObjectName("chatContainer")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Welcome message
        welcome_msg = self._create_chat_message(
            "Hello! I'm your AI assistant. How can I help you today?",
            is_user=False
        )
        self.chat_layout.addWidget(welcome_msg)
        
        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll)
        
        # Input area
        input_frame = QFrame()
        input_frame.setFixedHeight(80)
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 5, 0, 5)
        
        # Text input
        self.chat_input = QTextEdit()
        self.chat_input.setPlaceholderText("Type your message or command...")
        self.chat_input.setMaximumHeight(60)
        self.chat_input.setObjectName("chatInput")
        input_layout.addWidget(self.chat_input)
        
        # Send button
        send_btn = QPushButton("📤 Send")
        send_btn.setObjectName("primaryButton")
        send_btn.setFixedWidth(80)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_frame)
        
        # Voice controls
        voice_frame = self._create_voice_controls()
        layout.addWidget(voice_frame)
        
        return frame
    
    def _create_chat_message(self, text: str, is_user: bool = False) -> QFrame:
        """Create a chat message bubble."""
        bubble = QFrame()
        bubble.setObjectName("userBubble" if is_user else "aiBubble")
        bubble.setFixedHeight(60)
        
        layout = QVBoxLayout(bubble)
        layout.setContentsMargins(10, 10, 10, 10)
        
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        
        return bubble
    
    def _create_voice_controls(self) -> QFrame:
        """Create voice control buttons."""
        frame = QFrame()
        frame.setFixedHeight(40)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Voice input button
        voice_btn = QPushButton("🎤 Voice Input")
        voice_btn.setObjectName("accentButton")
        layout.addWidget(voice_btn)
        
        # Clear chat
        clear_btn = QPushButton("🗑️ Clear Chat")
        layout.addWidget(clear_btn)
        
        layout.addStretch()
        
        # Settings
        settings_btn = QPushButton("⚙️ AI Settings")
        layout.addWidget(settings_btn)
        
        return frame
