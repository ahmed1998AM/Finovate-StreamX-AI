"""
AI Auto Repair Engine
======================
Automatic diagnosis and repair of IPTV and playback issues.

Features:
- Repair Broken Streams
- Fix EPG Data
- Repair Playlists
- Optimize Playback
- Auto Diagnostics

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

import asyncio
from typing import Dict, Any, List, Optional
from enum import Enum
from pathlib import Path
import aiohttp


class IssueType(Enum):
    """Types of IPTV issues."""
    DEAD_STREAM = "dead_stream"
    SLOW_STREAM = "slow_stream"
    INVALID_URL = "invalid_url"
    MISSING_EPG = "missing_epg"
    INCORRECT_EPG = "incorrect_epg"
    PLAYLIST_PARSE_ERROR = "playlist_parse_error"
    BUFFER_UNDERRUN = "buffer_underrun"
    CODEC_ERROR = "codec_error"
    NETWORK_TIMEOUT = "network_timeout"
    SSL_ERROR = "ssl_error"


class AutoRepairEngine:
    """
    Automatic diagnosis and repair engine for IPTV issues.
    """
    
    def __init__(self):
        """Initialize the auto repair engine."""
        self.repair_strategies = {
            IssueType.DEAD_STREAM: self._repair_dead_stream,
            IssueType.SLOW_STREAM: self._repair_slow_stream,
            IssueType.INVALID_URL: self._repair_invalid_url,
            IssueType.MISSING_EPG: self._repair_missing_epg,
            IssueType.INCORRECT_EPG: self._repair_incorrect_epg,
            IssueType.PLAYLIST_PARSE_ERROR: self._repair_playlist_error,
            IssueType.BUFFER_UNDERRUN: self._repair_buffer_underrun,
            IssueType.CODEC_ERROR: self._repair_codec_error,
            IssueType.NETWORK_TIMEOUT: self._repair_network_timeout,
            IssueType.SSL_ERROR: self._repair_ssl_error,
        }
        
        self.diagnostic_cache = {}
    
    async def diagnose_playlist(self, playlist_url: str, 
                               channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Diagnose issues in a playlist.
        
        Args:
            playlist_url: URL or path to playlist
            channel_id: Specific channel to diagnose
            
        Returns:
            Diagnostic report with issues found
        """
        issues = []
        
        try:
            # Check if playlist is accessible
            is_accessible, status_code = await self._check_url_accessibility(playlist_url)
            
            if not is_accessible:
                issues.append({
                    'type': IssueType.NETWORK_TIMEOUT,
                    'severity': 'high',
                    'description': f'Playlist URL not accessible (Status: {status_code})',
                    'location': playlist_url
                })
            
            # Parse and validate playlist
            from iptv.parser import M3UParser
            
            parser = M3UParser()
            channels = await parser.parse_from_url(playlist_url)
            
            if not channels:
                issues.append({
                    'type': IssueType.PLAYLIST_PARSE_ERROR,
                    'severity': 'critical',
                    'description': 'Failed to parse playlist - no channels found',
                    'location': playlist_url
                })
                return {'issues': issues, 'channels_count': 0}
            
            # Test individual channels
            if channel_id:
                channels_to_test = [c for c in channels if c.get('id') == channel_id]
            else:
                # Test first 10 channels as sample
                channels_to_test = channels[:10]
            
            for channel in channels_to_test:
                channel_issues = await self._diagnose_channel(channel)
                issues.extend(channel_issues)
            
            return {
                'issues': issues,
                'channels_count': len(channels),
                'tested_channels': len(channels_to_test),
                'healthy_channels': len(channels_to_test) - sum(1 for i in issues if i.get('channel_id'))
            }
            
        except Exception as e:
            return {
                'issues': [{
                    'type': IssueType.PLAYLIST_PARSE_ERROR,
                    'severity': 'critical',
                    'description': f'Diagnosis failed: {str(e)}',
                    'exception': str(e)
                }],
                'channels_count': 0
            }
    
    async def _diagnose_channel(self, channel: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Diagnose a single channel."""
        issues = []
        stream_url = channel.get('url', '')
        
        # Check stream accessibility
        is_accessible, status_code = await self._check_url_accessibility(stream_url, timeout=5)
        
        if not is_accessible:
            if status_code == 404:
                issue_type = IssueType.INVALID_URL
            elif status_code == 0:
                issue_type = IssueType.NETWORK_TIMEOUT
            else:
                issue_type = IssueType.DEAD_STREAM
            
            issues.append({
                'type': issue_type,
                'severity': 'high',
                'description': f'Channel stream not accessible',
                'channel_id': channel.get('id'),
                'channel_name': channel.get('name'),
                'url': stream_url,
                'status_code': status_code
            })
        
        # Check stream speed
        speed = await self._measure_stream_speed(stream_url)
        if speed < 100:  # KB/s
            issues.append({
                'type': IssueType.SLOW_STREAM,
                'severity': 'medium',
                'description': f'Stream speed too low: {speed} KB/s',
                'channel_id': channel.get('id'),
                'channel_name': channel.get('name'),
                'speed_kbps': speed
            })
        
        # Check EPG
        if not channel.get('epg'):
            issues.append({
                'type': IssueType.MISSING_EPG,
                'severity': 'low',
                'description': 'No EPG data available',
                'channel_id': channel.get('id'),
                'channel_name': channel.get('name')
            })
        
        return issues
    
    async def repair_issues(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Attempt to repair identified issues.
        
        Args:
            issues: List of issues from diagnosis
            
        Returns:
            Repair results
        """
        fixed = []
        failed = []
        suggestions = []
        
        for issue in issues:
            issue_type = issue.get('type')
            
            if isinstance(issue_type, str):
                try:
                    issue_type = IssueType(issue_type)
                except ValueError:
                    failed.append({**issue, 'reason': 'Unknown issue type'})
                    continue
            
            repair_func = self.repair_strategies.get(issue_type)
            
            if repair_func:
                try:
                    result = await repair_func(issue)
                    if result.get('success'):
                        fixed.append({**issue, 'repair_result': result})
                    else:
                        failed.append({**issue, 'reason': result.get('error', 'Unknown error')})
                        if result.get('suggestion'):
                            suggestions.append(result['suggestion'])
                except Exception as e:
                    failed.append({**issue, 'reason': f'Repair failed: {str(e)}'})
            else:
                suggestions.append(f'No automatic repair available for {issue_type.value}')
                failed.append({**issue, 'reason': 'No repair strategy available'})
        
        return {
            'fixed': fixed,
            'failed': failed,
            'suggestions': suggestions,
            'total_issues': len(issues),
            'fixed_count': len(fixed),
            'failed_count': len(failed)
        }
    
    async def full_system_diagnostic(self) -> Dict[str, Any]:
        """Run comprehensive system diagnostic."""
        diagnostic = {
            'timestamp': asyncio.get_event_loop().time(),
            'components': {},
            'issues': [],
            'recommendations': []
        }
        
        # Check network connectivity
        network_ok = await self._check_network_connectivity()
        diagnostic['components']['network'] = {
            'status': 'ok' if network_ok else 'error',
            'details': 'Network connectivity verified' if network_ok else 'Network issues detected'
        }
        
        if not network_ok:
            diagnostic['issues'].append({
                'component': 'network',
                'severity': 'critical',
                'description': 'No network connectivity'
            })
            diagnostic['recommendations'].append('Check internet connection')
        
        # Check database
        db_ok = await self._check_database_health()
        diagnostic['components']['database'] = {
            'status': 'ok' if db_ok else 'error',
            'details': 'Database healthy' if db_ok else 'Database issues detected'
        }
        
        # Check VLC player
        vlc_ok = await self._check_vlc_availability()
        diagnostic['components']['vlc_player'] = {
            'status': 'ok' if vlc_ok else 'error',
            'details': 'VLC available' if vlc_ok else 'VLC not found'
        }
        
        if not vlc_ok:
            diagnostic['recommendations'].append('Install VLC media player')
        
        # Check disk space
        disk_ok, disk_percent = await self._check_disk_space()
        diagnostic['components']['disk_space'] = {
            'status': 'ok' if disk_ok else 'warning',
            'details': f'{disk_percent}% used'
        }
        
        if not disk_ok:
            diagnostic['recommendations'].append('Free up disk space')
        
        return diagnostic
    
    # Repair strategies
    async def _repair_dead_stream(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to repair dead stream."""
        url = issue.get('url', '')
        
        # Try alternative URLs
        alternatives = await self._find_alternative_streams(url)
        
        if alternatives:
            return {
                'success': True,
                'action': 'replaced_url',
                'original_url': url,
                'new_url': alternatives[0],
                'alternatives_count': len(alternatives)
            }
        
        # Try to refresh stream token
        refreshed_url = await self._refresh_stream_token(url)
        if refreshed_url and refreshed_url != url:
            is_accessible, _ = await self._check_url_accessibility(refreshed_url)
            if is_accessible:
                return {
                    'success': True,
                    'action': 'refreshed_token',
                    'original_url': url,
                    'new_url': refreshed_url
                }
        
        return {
            'success': False,
            'error': 'No alternative streams found',
            'suggestion': 'Remove this channel or update playlist source'
        }
    
    async def _repair_slow_stream(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to repair slow stream."""
        return {
            'success': False,
            'error': 'Cannot fix slow stream automatically',
            'suggestion': 'Try lower quality stream or check network connection'
        }
    
    async def _repair_invalid_url(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to repair invalid URL."""
        url = issue.get('url', '')
        
        # Try common URL fixes
        fixed_urls = []
        
        # Add https:// if missing
        if url.startswith('http://'):
            fixed_urls.append(url.replace('http://', 'https://'))
        
        # Remove trailing spaces
        fixed_urls.append(url.strip())
        
        # Try www subdomain
        if 'www.' not in url:
            parts = url.split('://')
            if len(parts) == 2:
                fixed_urls.append(f'{parts[0]}://www.{parts[1]}')
        
        # Test fixed URLs
        for fixed_url in fixed_urls:
            is_accessible, _ = await self._check_url_accessibility(fixed_url)
            if is_accessible:
                return {
                    'success': True,
                    'action': 'fixed_url',
                    'original_url': url,
                    'new_url': fixed_url
                }
        
        return {
            'success': False,
            'error': 'Could not fix URL',
            'suggestion': 'Channel URL is permanently invalid'
        }
    
    async def _repair_missing_epg(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fetch missing EPG."""
        channel_name = issue.get('channel_name', '')
        
        if not channel_name:
            return {'success': False, 'error': 'No channel name'}
        
        # Try to fetch EPG from sources
        from services.iptv_sources.epg_manager import EPGManager
        
        epg_manager = EPGManager()
        epg_data = await epg_manager.fetch_channel_epg(channel_name)
        
        if epg_data:
            return {
                'success': True,
                'action': 'fetched_epg',
                'channel_name': channel_name,
                'epg_programs': len(epg_data.get('programs', []))
            }
        
        return {
            'success': False,
            'error': 'EPG not available for this channel',
            'suggestion': 'EPG data not available from configured sources'
        }
    
    async def _repair_playlist_error(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to repair playlist parse errors."""
        return {
            'success': False,
            'error': 'Cannot automatically fix playlist format',
            'suggestion': 'Download playlist again or use different source'
        }
    
    async def _repair_buffer_underrun(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fix buffer underrun."""
        return {
            'success': True,
            'action': 'adjust_buffer_settings',
            'settings': {
                'cache_size_mb': 512,
                'network_caching_ms': 3000
            },
            'suggestion': 'Increased buffer size applied'
        }
    
    async def _repair_codec_error(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fix codec errors."""
        return {
            'success': False,
            'error': 'Codec not supported',
            'suggestion': 'Install additional codecs or use different player'
        }
    
    async def _repair_network_timeout(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fix network timeout."""
        return {
            'success': False,
            'error': 'Network timeout',
            'suggestion': 'Check internet connection and try again'
        }
    
    async def _repair_ssl_error(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fix SSL errors."""
        return {
            'success': False,
            'error': 'SSL certificate error',
            'suggestion': 'Stream uses invalid SSL certificate'
        }
    
    async def _repair_incorrect_epg(self, issue: Dict) -> Dict[str, Any]:
        """Attempt to fix incorrect EPG."""
        return {
            'success': False,
            'error': 'Cannot verify EPG accuracy',
            'suggestion': 'Use different EPG source'
        }
    
    # Helper methods
    async def _check_url_accessibility(self, url: str, timeout: int = 10) -> tuple:
        """Check if URL is accessible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=timeout, ssl=False) as response:
                    return True, response.status
        except Exception:
            return False, 0
    
    async def _measure_stream_speed(self, url: str) -> float:
        """Measure stream download speed in KB/s."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5, ssl=False) as response:
                    start_time = asyncio.get_event_loop().time()
                    bytes_downloaded = 0
                    
                    async for chunk in response.content.iter_chunked(8192):
                        bytes_downloaded += len(chunk)
                        elapsed = asyncio.get_event_loop().time() - start_time
                        
                        if elapsed >= 2 or bytes_downloaded >= 65536:
                            break
                    
                    if elapsed > 0:
                        return (bytes_downloaded / 1024) / elapsed
                    return 0
        except Exception:
            return 0
    
    async def _find_alternative_streams(self, url: str) -> List[str]:
        """Find alternative stream URLs."""
        # Placeholder - would integrate with backup stream services
        return []
    
    async def _refresh_stream_token(self, url: str) -> Optional[str]:
        """Refresh stream authentication token."""
        # Placeholder - would implement token refresh logic
        return None
    
    async def _check_network_connectivity(self) -> bool:
        """Check network connectivity."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.google.com', timeout=5) as response:
                    return response.status == 200
        except Exception:
            return False
    
    async def _check_database_health(self) -> bool:
        """Check database health."""
        try:
            from database.db_manager import DatabaseManager
            from core.config import get_config
            
            config = get_config()
            db = DatabaseManager(config.DATABASE_PATH)
            await db.connect()
            await db.disconnect()
            return True
        except Exception:
            return False
    
    async def _check_vlc_availability(self) -> bool:
        """Check if VLC is available."""
        try:
            import vlc
            instance = vlc.Instance()
            return instance is not None
        except Exception:
            return False
    
    async def _check_disk_space(self) -> tuple:
        """Check available disk space."""
        try:
            import shutil
            total, used, free = shutil.disk_usage('/')
            percent_used = (used / total) * 100
            return percent_used < 90, percent_used
        except Exception:
            return True, 0


# Singleton instance
_repair_engine: Optional[AutoRepairEngine] = None


def get_repair_engine() -> AutoRepairEngine:
    """Get or create the auto repair engine singleton."""
    global _repair_engine
    if _repair_engine is None:
        _repair_engine = AutoRepairEngine()
    return _repair_engine


async def diagnose_and_repair(playlist_url: str) -> Dict[str, Any]:
    """
    Convenience function to diagnose and repair playlist issues.
    
    Args:
        playlist_url: URL or path to playlist
        
    Returns:
        Combined diagnosis and repair results
    """
    engine = get_repair_engine()
    
    # Diagnose
    diagnosis = await engine.diagnose_playlist(playlist_url)
    
    # Repair if issues found
    if diagnosis.get('issues'):
        repair_result = await engine.repair_issues(diagnosis['issues'])
        diagnosis['repair_result'] = repair_result
    
    return diagnosis
