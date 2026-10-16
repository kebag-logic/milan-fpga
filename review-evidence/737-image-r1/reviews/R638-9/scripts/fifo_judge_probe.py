#!/usr/bin/env python3
"""Disposable reviewer probe: call the reviewed Origin.judge for a bash script operand that is a named pipe.
A writer thread supplies a checkout file's bytes once and closes; the provenance the audit assigns is
printed, then a second writer supplies other text, which is what an interpreter opening the pipe next reads.

Usage: python3 -I fifo_judge_probe.py <checkout> <scratch-dir>
"""
import json, os, sys, threading
from pathlib import Path

checkout, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "ci/image"))
import exec_audit  # noqa: E402

root = scratch / "checkout"
root.mkdir(parents=True)
(root / "ok.sh").write_text("echo reviewed\n")
fifo = scratch / "pipe"
os.mkfifo(fifo)
origin = exec_audit.Origin(root, exec_audit.allowlist(), scratch=(str(scratch),), watch=False)
writer = threading.Thread(target=lambda: fifo.write_text("echo reviewed\n"))
writer.start()
instance = {"pid": os.getpid(), "file": "/usr/bin/bash", "program": "/usr/bin/bash", "argv": ["bash", str(fifo)],
            "directory": str(scratch), "streams": {}}
origin.identify(instance)
provenance = origin.judge(instance)
writer.join()
later = threading.Thread(target=lambda: fifo.write_text("echo UNREVIEWED\n"))
later.start()
ran = fifo.read_text()
later.join()
print(json.dumps({"operand": "named pipe", "family": instance.get("family"), "provenance": provenance,
                  "audit_digest": instance.get("sha256"), "text_the_next_reader_gets": ran}, indent=1))
