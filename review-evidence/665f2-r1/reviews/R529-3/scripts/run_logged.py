#!/usr/bin/env python3
"""Run a foreground receipt command with a ten-minute bound."""
import argparse,json,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("log",type=Path);p.add_argument("command",nargs=argparse.REMAINDER);a=p.parse_args()
a.log.parent.mkdir(parents=True,exist_ok=True);start=time.monotonic()
with a.log.open("w") as f:
 f.write("argv: "+json.dumps(a.command)+"\n");f.flush()
 try: rc=subprocess.run(a.command,stdout=f,stderr=subprocess.STDOUT,timeout=590).returncode
 except subprocess.TimeoutExpired: rc=124
 f.write(f"\nexit={rc} elapsed_seconds={time.monotonic()-start:.3f}\n")
a.log.with_suffix(".rc").write_text(str(rc)+"\n");print(a.log.name,"exit",rc,flush=True)
raise SystemExit(rc)
