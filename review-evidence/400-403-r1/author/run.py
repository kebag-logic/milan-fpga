#!/usr/bin/env python3
"""Run a portable command with raw output and exact preliminary/final identity."""
import datetime, hashlib, json, os
from pathlib import Path
import subprocess, sys
out = Path(__file__).resolve().parent
label, *argv = sys.argv[1:]
assert argv and label.replace("-", "").replace("_", "").isalnum()
meta = dict(argv=argv, cwd=os.getcwd(), started=datetime.datetime.now(datetime.timezone.utc).isoformat())
for key, cmd in (("head", ["git", "rev-parse", "HEAD"]), ("tree", ["git", "rev-parse", "HEAD^{tree}"]), ("status", ["git", "status", "--porcelain=v1"]), ("diff", ["git", "diff", "HEAD", "--binary"])):
    result = subprocess.run(cmd, capture_output=True)
    if key == "diff":
        (out / (label + ".diff")).write_bytes(result.stdout)
        meta["diff_sha256"] = hashlib.sha256(result.stdout).hexdigest()
    else:
        meta[key] = result.stdout.decode()
meta["identity"] = "uncommitted working tree" if meta["status"] else "clean commit"
with (out / (label + ".log")).open("w") as log:
    result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT)
meta.update(exit=result.returncode, finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
meta['ending_head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
meta['ending_status'] = subprocess.check_output(['git', 'status', '--porcelain=v1'], text=True)
meta['ending_diff_sha256'] = hashlib.sha256(subprocess.check_output(['git', 'diff', 'HEAD', '--binary'])).hexdigest()
(out / (label + ".json")).write_text(json.dumps(meta, indent=2) + "\n")
print(json.dumps({k: meta[k] for k in ("argv", "head", "identity", "exit")}))
print((out / (label + ".log")).read_text()[-7000:])
sys.exit(result.returncode)
