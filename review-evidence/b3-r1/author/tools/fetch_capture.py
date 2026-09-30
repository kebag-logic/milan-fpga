#!/usr/bin/env python3
"""Copy one file off the SoC board over its serial console (this host; the
caller holds the bench lock).

usage: fetch_capture.py <board_path> <expected_sha256> <out_file> <transcript> [<timeout_s>]

The board prints `gzip -9 | base64` of the file between markers (its xz is a
decompress-only applet); this host rebuilds the file, checks the SHA-256 the
board computed when the file was written, and writes it only on a match.
Exit 0 on a verified copy, 2 otherwise. The board file is not removed here.

Environment: SOC_CONSOLE, A403_TOOLS (directory of soccon.py).
"""
import base64
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

soccon = Path(os.environ["A403_TOOLS"]) / "soccon.py"
path, want, out, log = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
limit = float(sys.argv[5]) if len(sys.argv) > 5 else 420.0
r = subprocess.run(["python3", str(soccon), os.environ["SOC_CONSOLE"], str(log), str(limit),
                    f"printf 'XF%s\\n' ER_BEGIN; gzip -9 -c {path} | base64; printf 'XF%s\\n' ER_END"],
                   timeout=limit + 30, capture_output=True)
text = log.read_bytes()
m = re.search(rb"\nXFER_BEGIN\r?\n(.*?)\r?\nXFER_END", text, re.S)
res = dict(board_path=path, soccon_rc=r.returncode, markers=m is not None)
if m:
    try:
        blob = gzip.decompress(base64.b64decode(re.sub(rb"\s", b"", m.group(1)), validate=True))
        res.update(b64_chars=len(re.sub(rb"\s", b"", m.group(1))), bytes=len(blob),
                   sha256=hashlib.sha256(blob).hexdigest(), expected=want)
        res["ok"] = res["sha256"] == want
        if res["ok"]:
            out.write_bytes(blob)
    except (ValueError, OSError, EOFError) as e:
        res.update(ok=False, error=repr(e)[:300])
else:
    res["ok"] = False
print(json.dumps(res))
sys.exit(0 if res["ok"] else 2)
