"""
AI Video Enhancement Module
============================
AI-powered video quality enhancement using deep learning.

Features:
- AI Upscaling (2x, 4x)
- Noise Reduction
- Frame Interpolation
- HDR Enhancement
- Sharpening

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import asyncio
from enum import Enum


class EnhancementType(Enum):
    """Types of video enhancement."""
    UPSCALE_2X = "upscale_2x"
    UPSCALE_4X = "upscale_4x"
    NOISE_REDUCTION = "noise_reduction"
    FRAME_INTERPOLATION = "frame_interpolation"
    HDR_ENHANCEMENT = "hdr_enhancement"
    SHARPENING = "sharpening"
    AUTO = "auto"


class VideoEnhancementEngine:
    """
    AI-powered video enhancement engine.
    
    Uses OpenCV and deep learning models for real-time video enhancement.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the video enhancement engine.
        
        Args:
            model_path: Path to AI models directory
        """
        self.model_path = Path(model_path) if model_path else Path(__file__).parent / "models"
        self.model_path.mkdir(parents=True, exist_ok=True)
        
        # Enhancement settings
        self.settings = {
            "upscale_factor": 2,
            "denoise_strength": 10,
            "interpolation_frames": 2,
            "hdr_intensity": 1.5,
            "sharpness": 1.2,
            "enable_gpu": True,
        }
        
        # Load models
        self.esrgan_model = None
        self.denoise_model = None
        self._load_models()
        
    def _load_models(self):
        """Load AI models for enhancement."""
        try:
            # Try to load ESRGAN for upscaling
            esrgan_path = self.model_path / "esrgan.pth"
            if esrgan_path.exists():
                # Load ESRGAN model (requires torch)
                try:
                    import torch
                    from basicsr.archs.rrdbnet_arch import RRDBNet
                    
                    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, 
                                   num_block=23, num_grow_ch=32, scale=4)
                    model.load_state_dict(torch.load(esrgan_path)['params_ema'], strict=True)
                    model.eval()
                    self.esrgan_model = model
                    print("ESRGAN model loaded successfully")
                except ImportError:
                    print("ESRGAN dependencies not installed, using OpenCV fallback")
            
            print("Video enhancement engine initialized")
        except Exception as e:
            print(f"Warning: Could not load AI models: {e}")
            print("Using OpenCV-based enhancement methods")
    
    async def enhance_frame(self, frame: np.ndarray, 
                           enhancement_type: EnhancementType = EnhancementType.AUTO) -> np.ndarray:
        """
        Enhance a single video frame.
        
        Args:
            frame: Input video frame (BGR format)
            enhancement_type: Type of enhancement to apply
            
        Returns:
            Enhanced frame
        """
        try:
            if enhancement_type == EnhancementType.AUTO:
                # Auto-detect best enhancement
                return await self._auto_enhance(frame)
            
            elif enhancement_type in [EnhancementType.UPSCALE_2X, EnhancementType.UPSCALE_4X]:
                return await self._upscale_frame(frame, enhancement_type)
            
            elif enhancement_type == EnhancementType.NOISE_REDUCTION:
                return self._denoise_frame(frame)
            
            elif enhancement_type == EnhancementType.SHARPENING:
                return self._sharpen_frame(frame)
            
            elif enhancement_type == EnhancementType.HDR_ENHANCEMENT:
                return self._enhance_hdr(frame)
            
            else:
                return frame
                
        except Exception as e:
            print(f"Enhancement error: {e}")
            return frame
    
    async def _auto_enhance(self, frame: np.ndarray) -> np.ndarray:
        """Auto-detect and apply best enhancement."""
        # Analyze frame quality
        height, width = frame.shape[:2]
        
        # Low resolution -> upscale
        if height < 720:
            return await self._upscale_frame(frame, EnhancementType.UPSCALE_2X)
        
        # High noise -> denoise
        if self._detect_noise_level(frame) > 0.3:
            frame = self._denoise_frame(frame)
        
        # Low sharpness -> sharpen
        if self._detect_sharpness(frame) < 0.5:
            frame = self._sharpen_frame(frame)
        
        return frame
    
    async def _upscale_frame(self, frame: np.ndarray, 
                            enhancement_type: EnhancementType) -> np.ndarray:
        """Upscale frame using AI or OpenCV."""
        scale = 4 if enhancement_type == EnhancementType.UPSCALE_4X else 2
        
        if self.esrgan_model is not None:
            # Use ESRGAN (requires GPU)
            try:
                import torch
                from torchvision import transforms
                
                # Convert to tensor
                transform = transforms.ToTensor()
                img_tensor = transform(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_tensor = img_tensor.unsqueeze(0)
                
                # Run inference
                with torch.no_grad():
                    output = self.esrgan_model(img_tensor)
                
                # Convert back to numpy
                output_np = output.squeeze().permute(1, 2, 0).numpy()
                output_np = (output_np * 255).astype(np.uint8)
                return cv2.cvtColor(output_np, cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"ESRGAN inference failed: {e}, falling back to OpenCV")
        
        # Fallback to OpenCV super-resolution
        return cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    def _denoise_frame(self, frame: np.ndarray) -> np.ndarray:
        """Apply noise reduction."""
        strength = self.settings["denoise_strength"]
        
        # FastNLMeansDenoisingColored for better quality
        denoised = cv2.fastNlMeansDenoisingColored(
            frame, None, 
            h=strength, 
            hForColorComponents=strength,
            templateWindowSize=7,
            searchWindowSize=21
        )
        
        return denoised
    
    def _sharpen_frame(self, frame: np.ndarray) -> np.ndarray:
        """Apply sharpening filter."""
        sharpness = self.settings["sharpness"]
        
        # Create sharpening kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5*sharpness, -1],
            [0, -1, 0]
        ])
        
        sharpened = cv2.filter2D(frame, -1, kernel)
        return sharpened
    
    def _enhance_hdr(self, frame: np.ndarray) -> np.ndarray:
        """Enhance HDR (High Dynamic Range)."""
        intensity = self.settings["hdr_intensity"]
        
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=intensity * 3.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        
        # Merge back
        lab_enhanced = cv2.merge([l_enhanced, a, b])
        enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def _detect_noise_level(self, frame: np.ndarray) -> float:
        """Detect noise level in frame (0.0 - 1.0)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate variance of Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalize to 0-1 range (higher variance = less noise)
        noise_level = 1.0 / (1.0 + variance / 1000.0)
        return min(noise_level, 1.0)
    
    def _detect_sharpness(self, frame: np.ndarray) -> float:
        """Detect sharpness level in frame (0.0 - 1.0)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate variance of Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalize to 0-1 range
        sharpness = min(variance / 500.0, 1.0)
        return sharpness
    
    async def enhance_video_file(self, input_path: str, output_path: str,
                                enhancement_type: EnhancementType = EnhancementType.AUTO,
                                progress_callback=None) -> bool:
        """
        Enhance entire video file.
        
        Args:
            input_path: Path to input video
            output_path: Path to save enhanced video
            enhancement_type: Type of enhancement
            progress_callback: Callback for progress updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cap = cv2.VideoCapture(input_path)
            
            if not cap.isOpened():
                print(f"Cannot open video: {input_path}")
                return False
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate output dimensions
            scale = self.settings["upscale_factor"]
            out_width = width * scale
            out_height = height * scale
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))
            
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Enhance frame
                enhanced = await self.enhance_frame(frame, enhancement_type)
                out.write(enhanced)
                
                frame_count += 1
                
                # Report progress
                if progress_callback:
                    progress = (frame_count / total_frames) * 100
                    await progress_callback(progress)
                
                # Allow other tasks to run
                if frame_count % 10 == 0:
                    await asyncio.sleep(0.01)
            
            cap.release()
            out.release()
            
            print(f"Video enhancement complete: {output_path}")
            return True
            
        except Exception as e:
            print(f"Video enhancement failed: {e}")
            return False
    
    def update_settings(self, **kwargs):
        """Update enhancement settings."""
        self.settings.update(kwargs)
        print(f"Enhancement settings updated: {self.settings}")


# Singleton instance
_enhancement_engine: Optional[VideoEnhancementEngine] = None


def get_enhancement_engine() -> VideoEnhancementEngine:
    """Get or create the video enhancement engine singleton."""
    global _enhancement_engine
    if _enhancement_engine is None:
        _enhancement_engine = VideoEnhancementEngine()
    return _enhancement_engine


async def enhance_stream(frame: np.ndarray, **kwargs) -> np.ndarray:
    """
    Convenience function to enhance a video stream frame.
    
    Args:
        frame: Input frame
        **kwargs: Additional arguments for enhancement
        
    Returns:
        Enhanced frame
    """
    engine = get_enhancement_engine()
    enhancement_type = kwargs.get('enhancement_type', EnhancementType.AUTO)
    return await engine.enhance_frame(frame, enhancement_type)
