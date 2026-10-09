#!/usr/bin/env python3
"""Run the unchanged earlier public probes at the current head."""
import pathlib, subprocess, sys
root, packet = map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
for name in ("r565-1","r564-1-full","r564-2"):
 subprocess.run([sys.executable,"-B",str(packet/"scripts/run_probes.py"),str(root),str(packet),name],check=True)
