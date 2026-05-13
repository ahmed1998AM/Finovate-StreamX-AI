"""
AI Assistant Module
===================
Multi-provider AI assistant for StreamX application.
"""

from typing import Optional, Dict, Any, List, AsyncGenerator
from abc import ABC, abstractmethod
import asyncio


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    async def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Send a chat message and get response."""
        pass
    
    @abstractmethod
    async def stream_chat(self, message: str, context: Optional[List[Dict]] = None) -> AsyncGenerator[str, None]:
        """Stream chat response."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if provider is available."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API provider implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        """Lazy load OpenAI client."""
        if self._client is None:
            try:
                from langchain_openai import ChatOpenAI
                self._client = ChatOpenAI(
                    api_key=self.api_key,
                    model=self.model,
                    temperature=0.7
                )
            except ImportError:
                raise ImportError("langchain-openai not installed")
        return self._client
    
    async def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Send chat message to OpenAI."""
        client = self._get_client()
        
        messages = context or []
        messages.append({"role": "user", "content": message})
        
        response = await asyncio.to_thread(client.invoke, messages)
        return response.content
    
    async def stream_chat(self, message: str, context: Optional[List[Dict]] = None) -> AsyncGenerator[str, None]:
        """Stream chat response from OpenAI."""
        client = self._get_client()
        
        messages = context or []
        messages.append({"role": "user", "content": message})
        
        for chunk in client.stream(messages):
            yield chunk.content
    
    async def is_available(self) -> bool:
        """Check OpenAI availability."""
        try:
            self._get_client()
            return True
        except Exception:
            return False


class OllamaProvider(AIProvider):
    """Ollama local LLM provider."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self._client = None
    
    async def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Send chat message to Ollama."""
        import aiohttp
        
        messages = context or []
        messages.append({"role": "user", "content": message})
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                }
            ) as response:
                data = await response.json()
                return data.get("message", {}).get("content", "")
    
    async def stream_chat(self, message: str, context: Optional[List[Dict]] = None) -> AsyncGenerator[str, None]:
        """Stream chat response from Ollama."""
        import aiohttp
        
        messages = context or []
        messages.append({"role": "user", "content": message})
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True
                }
            ) as response:
                async for line in response.content:
                    if line:
                        import json
                        try:
                            data = json.loads(line)
                            yield data.get("message", {}).get("content", "")
                        except json.JSONDecodeError:
                            pass
    
    async def is_available(self) -> bool:
        """Check Ollama availability."""
        import aiohttp
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    return response.status == 200
        except Exception:
            return False


class StreamXAssistant:
    """Main AI assistant for StreamX application."""
    
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {}
        self.current_provider: Optional[str] = None
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_length = 20
    
    def register_provider(self, name: str, provider: AIProvider):
        """
        Register an AI provider.
        
        Args:
            name: Provider name identifier
            provider: AIProvider instance
        """
        self.providers[name] = provider
        if not self.current_provider:
            self.current_provider = name
    
    def set_provider(self, name: str):
        """Set the current AI provider."""
        if name in self.providers:
            self.current_provider = name
        else:
            raise ValueError(f"Provider '{name}' not found")
    
    def get_current_provider(self) -> Optional[AIProvider]:
        """Get current AI provider instance."""
        if self.current_provider:
            return self.providers.get(self.current_provider)
        return None
    
    async def chat(self, message: str, use_context: bool = True) -> str:
        """
        Send a chat message.
        
        Args:
            message: User message
            use_context: Whether to include conversation history
            
        Returns:
            AI response string
        """
        provider = self.get_current_provider()
        if not provider:
            return "No AI provider configured. Please configure an AI provider in settings."
        
        context = self.conversation_history.copy() if use_context else None
        response = await provider.chat(message, context)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
        
        return response
    
    async def stream_chat(self, message: str, use_context: bool = True) -> AsyncGenerator[str, None]:
        """Stream AI response."""
        provider = self.get_current_provider()
        if not provider:
            yield "No AI provider configured."
            return
        
        context = self.conversation_history.copy() if use_context else None
        
        full_response = ""
        async for chunk in provider.stream_chat(message, context):
            full_response += chunk
            yield chunk
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": full_response})
        
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
    
    async def check_availability(self) -> Dict[str, bool]:
        """Check availability of all registered providers."""
        results = {}
        for name, provider in self.providers.items():
            results[name] = await provider.is_available()
        return results
    
    # IPTV-specific AI helpers
    async def help_with_playlist(self, issue: str) -> str:
        """Get AI help with playlist issues."""
        message = f"""You are an IPTV expert assistant. Help the user with this playlist issue:
        
Issue: {issue}

Provide specific troubleshooting steps and solutions."""
        
        return await self.chat(message, use_context=False)
    
    async def suggest_channels(self, preferences: str) -> str:
        """Get channel suggestions based on preferences."""
        message = f"""You are an IPTV assistant. Based on these viewing preferences, suggest channel categories and types:

Preferences: {preferences}

Provide helpful recommendations."""
        
        return await self.chat(message, use_context=False)
    
    async def explain_stream_error(self, error: str) -> str:
        """Get explanation for streaming errors."""
        message = f"""You are a technical support assistant for IPTV streaming. Explain this error and provide solutions:

Error: {error}

Give clear, actionable troubleshooting steps."""
        
        return await self.chat(message, use_context=False)
    
    def get_iptv_assistant_prompt(self) -> str:
        """Get system prompt for IPTV assistant mode."""
        return """You are StreamX AI Assistant, a specialized AI helper for IPTV and media streaming.

Your capabilities include:
- Helping users configure and troubleshoot IPTV playlists
- Explaining streaming protocols (HLS, DASH, RTMP, etc.)
- Assisting with EPG setup and configuration
- Providing codec and format compatibility information
- Helping with player settings optimization
- Suggesting solutions for common streaming issues

Always provide clear, step-by-step instructions and be specific about technical details."""
