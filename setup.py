"""
Run this script once to create a .venv and install plugin dependencies:

    python setup.py
"""

import subprocess
import sys
from pathlib import Path

plugin_dir = Path(__file__).parent
venv_dir = plugin_dir / ".venv"
requirements = plugin_dir / "requirements.txt"

print(f"Creating virtual environment at {venv_dir} ...")
subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

venv_python = venv_dir / "Scripts" / "python.exe"
if not venv_python.exists():
    venv_python = venv_dir / "bin" / "python"

print("Installing requirements ...")
subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(requirements)], check=True)

print("\nSetup complete. You can now launch Meshroom.")
