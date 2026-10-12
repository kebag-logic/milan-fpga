#!/usr/bin/env python3
"""Reproduce R629-1-F01 without editing source or running a full bank."""
import argparse,os,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);a=ap.parse_args()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
raise SystemExit(subprocess.call(["python3","-m","behave","features/counters_contract_milan.feature","--name","the bind edge wipes all ten, and the unbind edge wipes none","--no-capture","-f","plain"],cwd=a.root/"tests",env=env))
