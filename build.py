"""
Build Script for Finovate StreamX AI
=====================================
Nuitka-based build script with UPX compression for optimized Windows EXE.
"""

import os
import sys
import shutil
from pathlib import Path


def get_nuitka_command() -> str:
    """Generate Nuitka build command."""
    
    # Project paths
    project_root = Path(__file__).parent
    main_file = project_root / "main.py"
    output_dir = project_root / "dist"
    icon_path = project_root / "assets" / "icon.ico"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build command components
    cmd_parts = [
        "python -m nuitka",
        
        # Main file
        f'"{main_file}"',
        
        # Output settings
        f'--output-dir="{output_dir}"',
        "--onefile",
        "--windows-console-mode=disable",
        
        # Product info
        '--product-name="Finovate StreamX AI"',
        '--file-version="1.0.0"',
        '--product-version="1.0.0"',
        '--company-name="Finovate – AHMED EG"',
        '--file-description="Ultimate AI IPTV & Media Center"',
        '--copyright="© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved"',
        
        # Icon
        f'--windows-icon-from-ico="{icon_path}"' if icon_path.exists() else "",
        
        # Optimization
        "--optimize=O3",
        "--enable-lto=true",
        "--remove-console",
        
        # Module inclusion
        "--include-module=PySide6",
        "--include-module=aiohttp",
        "--include-module=aiosqlite",
        "--include-module=langchain",
        "--include-module=requests",
        
        # Module exclusion (reduce size)
        "--nofollow-imports",
        "--nofollow-import-to=tkinter",
        "--nofollow-import-to=test",
        "--nofollow-import-to=tests",
        "--nofollow-import-to=pip",
        
        # Data files
        f'--include-data-dir="{project_root}/ui"="ui"',
        f'--include-data-dir="{project_root}/assets"="assets"',
        
        # UPX compression
        "--enable-plugin=upx",
        
        # Windows specific
        "--windows-disable-console",
        "--assume-yes-for-downloads",
    ]
    
    # Filter empty parts
    cmd_parts = [p for p in cmd_parts if p]
    
    return " ".join(cmd_parts)


def cleanup_build():
    """Clean up build artifacts."""
    project_root = Path(__file__).parent
    
    # Directories to clean
    clean_dirs = [
        project_root / "build",
        project_root / "dist",
        project_root / "__pycache__",
    ]
    
    for dir_path in clean_dirs:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"Cleaned: {dir_path}")


def check_dependencies():
    """Check if required build dependencies are installed."""
    missing = []
    
    try:
        import nuitka
    except ImportError:
        missing.append("nuitka")
    
    try:
        import PySide6
    except ImportError:
        missing.append("PySide6")
    
    if missing:
        print("Missing build dependencies:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    
    return True


def build():
    """Main build function."""
    print("=" * 60)
    print("Finovate StreamX AI - Build Script")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("Checking build dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies found")
    print()
    
    # Clean previous build
    print("Cleaning previous build artifacts...")
    cleanup_build()
    print()
    
    # Generate and run build command
    print("Generating build command...")
    cmd = get_nuitka_command()
    print(f"Command: {cmd}")
    print()
    
    print("Starting build process...")
    print("This may take several minutes...")
    print()
    
    os.system(cmd)
    
    print()
    print("=" * 60)
    print("Build complete!")
    print("Output location: dist/")
    print("=" * 60)


if __name__ == "__main__":
    build()
