"""
Finovate StreamX AI - DVR Recording System
Live TV Recording, Scheduled Recording, Cloud Recording
Developer: Ahmed Mostafa Ibrahim | Finovate – AHMED EG
"""

import os
import asyncio
import threading
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import json
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Recording:
    """Recording metadata"""
    id: str
    channel_name: str
    channel_url: str
    start_time: str
    end_time: str
    duration_seconds: int
    file_path: str
    status: str  # scheduled, recording, completed, failed
    created_at: str
    size_mb: float = 0.0


class DVRManager:
    """Digital Video Recorder Manager for live TV recording"""
    
    def __init__(self, recordings_dir: str = None):
        self.recordings_dir = Path(recordings_dir) if recordings_dir else Path.home() / "StreamX_Recordings"
        self.recordings_dir.mkdir(exist_ok=True)
        
        self.recordings: Dict[str, Recording] = {}
        self.scheduled_recordings: Dict[str, Recording] = {}
        self.active_recordings: Dict[str, dict] = {}
        self.recording_processes: Dict[str, subprocess.Popen] = {}
        
        self.max_simultaneous_recordings = 4
        self.default_duration_minutes = 120
        self.auto_trim_completed = True
        
        # Load existing recordings
        self._load_recordings_index()
    
    def _load_recordings_index(self):
        """Load recordings index from disk"""
        index_file = self.recordings_dir / "recordings_index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for rec_id, rec_data in data.items():
                        self.recordings[rec_id] = Recording(**rec_data)
                logger.info(f"Loaded {len(self.recordings)} existing recordings")
            except Exception as e:
                logger.error(f"Failed to load recordings index: {e}")
    
    def _save_recordings_index(self):
        """Save recordings index to disk"""
        index_file = self.recordings_dir / "recordings_index.json"
        try:
            data = {rec_id: asdict(rec) for rec_id, rec in self.recordings.items()}
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save recordings index: {e}")
    
    def schedule_recording(
        self,
        channel_name: str,
        channel_url: str,
        start_time: datetime,
        duration_minutes: int = None,
        recording_id: str = None
    ) -> Recording:
        """Schedule a new recording"""
        if duration_minutes is None:
            duration_minutes = self.default_duration_minutes
        
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        if recording_id is None:
            recording_id = f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{channel_name.replace(' ', '_')}"
        
        recording = Recording(
            id=recording_id,
            channel_name=channel_name,
            channel_url=channel_url,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=duration_minutes * 60,
            file_path=str(self.recordings_dir / f"{recording_id}.mp4"),
            status="scheduled",
            created_at=datetime.now().isoformat()
        )
        
        self.scheduled_recordings[recording_id] = recording
        logger.info(f"Scheduled recording: {channel_name} at {start_time}")
        
        return recording
    
    def start_live_recording(
        self,
        channel_name: str,
        channel_url: str,
        duration_minutes: int = None,
        recording_id: str = None
    ) -> Recording:
        """Start recording live TV immediately"""
        return self.schedule_recording(
            channel_name=channel_name,
            channel_url=channel_url,
            start_time=datetime.now(),
            duration_minutes=duration_minutes,
            recording_id=recording_id
        )
    
    async def execute_recording(self, recording: Recording):
        """Execute a scheduled or live recording using FFmpeg"""
        if len(self.active_recordings) >= self.max_simultaneous_recordings:
            logger.warning("Maximum simultaneous recordings reached")
            return
        
        recording.status = "recording"
        self.active_recordings[recording.id] = asdict(recording)
        self.recordings[recording.id] = recording
        self._save_recordings_index()
        
        try:
            # FFmpeg command for recording
            cmd = [
                'ffmpeg',
                '-i', recording.channel_url,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-bsf:a', 'aac_adtstoasc',
                '-movflags', '+frag_keyframe+empty_moov',
                '-y',  # Overwrite output file
                recording.file_path
            ]
            
            logger.info(f"Starting recording: {recording.channel_name}")
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            self.recording_processes[recording.id] = process
            
            # Monitor recording
            await self._monitor_recording(recording, process)
            
        except Exception as e:
            logger.error(f"Recording failed for {recording.channel_name}: {e}")
            recording.status = "failed"
            self.recordings[recording.id] = recording
            self._save_recordings_index()
        finally:
            # Cleanup
            if recording.id in self.active_recordings:
                del self.active_recordings[recording.id]
            if recording.id in self.recording_processes:
                del self.recording_processes[recording.id]
    
    async def _monitor_recording(self, recording: Recording, process: subprocess.Popen):
        """Monitor recording progress and handle completion"""
        start_time = datetime.now()
        max_duration = timedelta(seconds=recording.duration_seconds)
        
        while process.poll() is None:
            elapsed = datetime.now() - start_time
            
            # Check if recording should stop
            if elapsed >= max_duration:
                logger.info(f"Stopping recording: {recording.channel_name} (duration reached)")
                process.terminate()
                break
            
            # Update file size
            if os.path.exists(recording.file_path):
                recording.size_mb = os.path.getsize(recording.file_path) / (1024 * 1024)
            
            await asyncio.sleep(5)
        
        # Finalize recording
        recording.status = "completed"
        if os.path.exists(recording.file_path):
            recording.size_mb = os.path.getsize(recording.file_path) / (1024 * 1024)
        
        self.recordings[recording.id] = recording
        self._save_recordings_index()
        logger.info(f"Recording completed: {recording.channel_name} ({recording.size_mb:.2f} MB)")
    
    def stop_recording(self, recording_id: str) -> bool:
        """Stop an active recording"""
        if recording_id not in self.recording_processes:
            return False
        
        process = self.recording_processes[recording_id]
        process.terminate()
        
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        
        logger.info(f"Stopped recording: {recording_id}")
        return True
    
    def cancel_scheduled_recording(self, recording_id: str) -> bool:
        """Cancel a scheduled recording"""
        if recording_id in self.scheduled_recordings:
            del self.scheduled_recordings[recording_id]
            logger.info(f"Cancelled scheduled recording: {recording_id}")
            return True
        return False
    
    def get_recordings(self, status: str = None) -> List[Recording]:
        """Get list of recordings filtered by status"""
        if status:
            return [rec for rec in self.recordings.values() if rec.status == status]
        return list(self.recordings.values())
    
    def get_scheduled_recordings(self) -> List[Recording]:
        """Get all scheduled recordings"""
        return list(self.scheduled_recordings.values())
    
    def delete_recording(self, recording_id: str) -> bool:
        """Delete a recording and its file"""
        if recording_id not in self.recordings:
            return False
        
        recording = self.recordings[recording_id]
        
        # Delete file
        if os.path.exists(recording.file_path):
            os.remove(recording.file_path)
        
        # Remove from index
        del self.recordings[recording_id]
        self._save_recordings_index()
        
        logger.info(f"Deleted recording: {recording_id}")
        return True
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics for recordings"""
        total_size = sum(rec.size_mb for rec in self.recordings.values() if rec.status == "completed")
        file_count = len([rec for rec in self.recordings.values() if rec.status == "completed"])
        
        return {
            'total_recordings': len(self.recordings),
            'completed_recordings': file_count,
            'scheduled_recordings': len(self.scheduled_recordings),
            'active_recordings': len(self.active_recordings),
            'total_size_mb': total_size,
            'total_size_gb': total_size / 1024,
            'storage_path': str(self.recordings_dir)
        }
    
    async def run_scheduler(self):
        """Background scheduler to execute scheduled recordings"""
        logger.info("DVR Scheduler started")
        
        while True:
            now = datetime.now()
            
            # Check scheduled recordings
            for rec_id, recording in list(self.scheduled_recordings.items()):
                start_time = datetime.fromisoformat(recording.start_time)
                
                if start_time <= now:
                    # Time to start recording
                    logger.info(f"Starting scheduled recording: {recording.channel_name}")
                    del self.scheduled_recordings[rec_id]
                    
                    # Start recording in background
                    asyncio.create_task(self.execute_recording(recording))
            
            await asyncio.sleep(10)  # Check every 10 seconds


class CloudRecordingManager:
    """Manage cloud recording storage and sync"""
    
    def __init__(self, dvr_manager: DVRManager):
        self.dvr_manager = dvr_manager
        self.cloud_providers = []  # Supabase, Google Drive, etc.
        self.auto_upload = False
        self.upload_queue: List[str] = []
    
    def enable_cloud_upload(self, provider: str, credentials: dict):
        """Enable automatic cloud upload for recordings"""
        self.cloud_providers.append({
            'provider': provider,
            'credentials': credentials,
            'enabled': True
        })
        self.auto_upload = True
        logger.info(f"Cloud upload enabled for {provider}")
    
    async def upload_recording(self, recording_id: str):
        """Upload a recording to cloud storage"""
        if recording_id not in self.dvr_manager.recordings:
            return False
        
        recording = self.dvr_manager.recordings[recording_id]
        
        if not os.path.exists(recording.file_path):
            logger.error(f"Recording file not found: {recording.file_path}")
            return False
        
        # Upload to each enabled cloud provider
        for provider_config in self.cloud_providers:
            if not provider_config['enabled']:
                continue
            
            try:
                # Placeholder for actual cloud upload logic
                logger.info(f"Uploading {recording.channel_name} to {provider_config['provider']}")
                # TODO: Implement actual upload using cloud SDKs
            except Exception as e:
                logger.error(f"Cloud upload failed: {e}")
        
        return True
    
    def queue_for_upload(self, recording_id: str):
        """Add recording to upload queue"""
        if recording_id not in self.upload_queue:
            self.upload_queue.append(recording_id)
            logger.info(f"Added {recording_id} to cloud upload queue")
    
    async def process_upload_queue(self):
        """Process cloud upload queue"""
        while self.upload_queue:
            recording_id = self.upload_queue.pop(0)
            await self.upload_recording(recording_id)
            await asyncio.sleep(1)  # Delay between uploads


# Example usage
if __name__ == "__main__":
    dvr = DVRManager()
    
    # Schedule a recording
    future_time = datetime.now() + timedelta(minutes=1)
    recording = dvr.schedule_recording(
        channel_name="Test Channel",
        channel_url="http://example.com/stream.m3u8",
        start_time=future_time,
        duration_minutes=30
    )
    
    print(f"Scheduled: {recording}")
    print(f"Storage stats: {dvr.get_storage_stats()}")
