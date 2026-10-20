#!/usr/bin/env python3
"""Verify the unchanged public receipts retained in this review packet."""
import hashlib, json, pathlib, sys, urllib.request
root=pathlib.Path(__file__).resolve().parent
for row in json.loads((root/"receipt-provenance.json").read_text()):
    data=(root/row["file"]).read_bytes()
    assert hashlib.sha256(data).hexdigest()==row["sha256"],row["file"]
    if "--online" in sys.argv:
        remote=urllib.request.urlopen(row["url"],timeout=60).read()
        assert remote==data,row["url"]
print("PASS: all retained public receipts match recorded SHA-256 values")
