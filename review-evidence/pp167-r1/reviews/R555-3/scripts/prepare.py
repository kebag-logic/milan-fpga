#!/usr/bin/env python3
"""Prepare packet-local Python dependencies; no shared installation is changed."""
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parents[1]
venv = packet / "scratch/venv"
subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
subprocess.run([str(venv / "bin/python"), "-m", "pip", "install", "wavedrom==2.0.3.post3"], check=True)
