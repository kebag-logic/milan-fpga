#!/usr/bin/env python3
"""Preserve one foreground command's raw output, status and elapsed time."""
import argparse,json,pathlib,subprocess,time
p=argparse.ArgumentParser();p.add_argument("prefix",type=pathlib.Path);p.add_argument("command",nargs=argparse.REMAINDER);a=p.parse_args()
start=time.monotonic()
with a.prefix.with_suffix(".log").open("w") as f:rc=subprocess.run(a.command,stdout=f,stderr=subprocess.STDOUT).returncode
record={"command":a.command,"rc":rc,"wall_seconds":time.monotonic()-start}
a.prefix.with_suffix(".rc").write_text(str(rc)+"\n");a.prefix.with_suffix(".json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record));raise SystemExit(rc)
