#!/usr/bin/env python3
"""Run one foreground command, retaining its unpiped output and exit status."""
import argparse, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--cwd",type=Path,required=True);p.add_argument("--out",type=Path,required=True);p.add_argument("command",nargs=argparse.REMAINDER);a=p.parse_args()
a.out.parent.mkdir(parents=True,exist_ok=True)
start=time.monotonic()
with a.out.with_suffix(".log").open("wb") as log:
 r=subprocess.run(a.command,cwd=a.cwd,stdout=log,stderr=subprocess.STDOUT)
a.out.with_suffix(".rc").write_text(str(r.returncode)+"\n")
a.out.with_suffix(".seconds").write_text(f"{time.monotonic()-start:.3f}\n")
print(f"{a.out.name}: rc={r.returncode}; elapsed={time.monotonic()-start:.1f}s")
raise SystemExit(r.returncode)
