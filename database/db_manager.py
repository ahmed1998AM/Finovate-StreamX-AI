"""
Database Manager Module
=======================
Async SQLite database manager with connection pooling.
"""

import aiosqlite
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from contextlib import asynccontextmanager
import asyncio


class DatabaseManager:
    """Async SQLite database manager for StreamX application."""
    
    def __init__(self, db_path: Path):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._connection: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()
    
    async def connect(self):
        """Establish database connection."""
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            await self._connection.execute("PRAGMA journal_mode=WAL")
            await self._connection.execute("PRAGMA synchronous=NORMAL")
            await self._connection.execute("PRAGMA cache_size=10000")
            await self._connection.commit()
    
    async def disconnect(self):
        """Close database connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
    
    @asynccontextmanager
    async def get_cursor(self):
        """Get database cursor with automatic commit."""
        if self._connection is None:
            await self.connect()
        
        cursor = await self._connection.cursor()
        try:
            yield cursor
            await self._connection.commit()
        except Exception as e:
            await self._connection.rollback()
            raise e
    
    async def execute(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> int:
        """
        Execute a write query (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        async with self._lock:
            async with self.get_cursor() as cursor:
                if params:
                    await cursor.execute(query, params)
                else:
                    await cursor.execute(query)
                return cursor.rowcount
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch one row from database.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Single row as dictionary or None
        """
        async with self.get_cursor() as cursor:
            if params:
                await cursor.execute(query, params)
            else:
                await cursor.execute(query)
            
            row = await cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all rows from database.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of rows as dictionaries
        """
        async with self.get_cursor() as cursor:
            if params:
                await cursor.execute(query, params)
            else:
                await cursor.execute(query)
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    async def fetch_many(
        self,
        query: str,
        limit: int,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch limited number of rows.
        
        Args:
            query: SQL query string
            limit: Maximum number of rows to fetch
            params: Query parameters
            
        Returns:
            List of rows as dictionaries
        """
        query = f"{query} LIMIT {limit}"
        return await self.fetch_all(query, params)
    
    async def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = await self.fetch_one(query, (table_name,))
        return result is not None
    
    async def drop_table(self, table_name: str):
        """Drop a table if it exists."""
        await self.execute(f"DROP TABLE IF EXISTS {table_name}")


# Table schemas
TABLE_SCHEMAS = {
    "playlists": """
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT,
            file_path TEXT,
            format TEXT DEFAULT 'M3U',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            auto_refresh BOOLEAN DEFAULT 0,
            refresh_interval_hours INTEGER DEFAULT 24
        )
    """,
    
    "channels": """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id INTEGER,
            name TEXT NOT NULL,
            logo_url TEXT,
            category TEXT,
            country TEXT,
            language TEXT,
            quality TEXT,
            stream_url TEXT NOT NULL,
            epg_id TEXT,
            group_title TEXT,
            is_favorite BOOLEAN DEFAULT 0,
            last_watched TIMESTAMP,
            watch_count INTEGER DEFAULT 0,
            FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE
        )
    """,
    
    "epg": """
        CREATE TABLE IF NOT EXISTS epg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            category TEXT,
            icon_url TEXT,
            rating TEXT,
            FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
        )
    """,
    
    "watch_history": """
        CREATE TABLE IF NOT EXISTS watch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER,
            user_id TEXT DEFAULT 'default',
            watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_seconds INTEGER,
            position_seconds INTEGER DEFAULT 0,
            FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
        )
    """,
    
    "favorites": """
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER UNIQUE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE
        )
    """,
    
    "settings": """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    
    "ai_conversations": """
        CREATE TABLE IF NOT EXISTS ai_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        )
    """,
    
    "plugins": """
        CREATE TABLE IF NOT EXISTS plugins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            version TEXT,
            enabled BOOLEAN DEFAULT 1,
            config TEXT,
            installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
}


async def initialize_database(db_manager: DatabaseManager):
    """Initialize database with all required tables."""
    for table_name, schema in TABLE_SCHEMAS.items():
        if not await db_manager.table_exists(table_name):
            await db_manager.execute(schema)
    
    # Insert default settings
    default_settings = {
        "theme": "dark_neon",
        "language": "en",
        "volume": "80",
        "hardware_acceleration": "true",
        "auto_update": "true"
    }
    
    for key, value in default_settings.items():
        await db_manager.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
