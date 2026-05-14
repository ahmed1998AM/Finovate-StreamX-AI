"""
Build Executable for Finovate StreamX AI
=========================================
PyInstaller-based build script to create standalone executable.
"""

import os
import sys
import shutil
from pathlib import Path

def get_pyinstaller_command() -> str:
    """Generate PyInstaller build command."""
    
    # Project paths
    project_root = Path(__file__).parent
    main_file = project_root / "main.py"
    output_dir = project_root / "dist"
    icon_path = project_root / "assets" / "icon.ico"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build command components
    cmd_parts = [
        "pyinstaller",
        
        # Main file
        f'"{main_file}"',
        
        # Output settings
        f'--distpath="{output_dir}"',
        "--onefile",
        "--noconfirm",
        "--clean",
        
        # Product info
        '--name="Finovate-StreamX-AI"',
        
        # Icon
        f'--icon="{icon_path}"' if icon_path.exists() else "",
        
        # Hidden imports
        "--hidden-import=PySide6",
        "--hidden-import=aiohttp",
        "--hidden-import=aiosqlite",
        "--hidden-import=requests",
        "--hidden-import=langchain",
        
        # Data files
        f'--add-data="{project_root}/ui{os.pathsep}ui"',
        f'--add-data="{project_root}/assets{os.pathsep}assets"',
        f'--add-data="{project_root}/core{os.pathsep}core"',
        f'--add-data="{project_root}/database{os.pathsep}database"',
        
        # Exclude unnecessary modules
        "--exclude-module=tkinter",
        "--exclude-module=test",
        "--exclude-module=pip",
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
        import PyInstaller
    except ImportError:
        missing.append("pyinstaller")
    
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
    print("Finovate StreamX AI - Build Executable")
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
    cmd = get_pyinstaller_command()
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
