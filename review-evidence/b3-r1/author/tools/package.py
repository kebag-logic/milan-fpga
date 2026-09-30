#!/usr/bin/env python3
"""Assemble the lane B3 packet: copy per-action evidence, redact private
identifiers, and index every raw file (offline, no bench access).

usage: package.py <packet_dir> <raw_root> <private_map_json>

1. Per action (din-long, dout-long, usb-long, usb-long2): copy every file of
   <raw_root>/<action>/ into <packet>/runs/<action>/, except the captures
   (.pcap, .raw) and any file over 200 KB. A grade.json over the limit is
   written as grade-summary.json without its per-segment lists.
2. The controller's per-action logs (<raw_root>/controller-staging/, not the
   tool copies) go to <packet>/runs/controller/.
3. Every text file in the packet's evidence directories (identity, restore,
   soc, runs, summary) is redacted with the private map: bench host names,
   interface names, controller, peer and grandmaster identifiers, bridge
   network addresses and the account name become role labels. The original
   of each changed file is kept under <raw_root>/packet-originals/.
   redaction.json lists, per file, the original and retained SHA-256 and the
   labels used; it never lists the private values.
4. RAW-ARTIFACTS.json lists every file under <raw_root> by relative path,
   size and SHA-256.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

P, RAW, MAP = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
LIMIT = 200 * 1024
m = json.loads(MAP.read_text())
LIT = [(re.compile(re.escape(a), re.IGNORECASE), b) for a, b in m["literal"]]
RX = [(re.compile(a), b) for a, b in m["regex"]]


def sha(b):
    return hashlib.sha256(b).hexdigest()


# 1 and 2: copies
for act in ("din-long", "dout-long", "usb-long", "usb-long2"):
    dst = P / "runs" / act
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted((RAW / act).iterdir()):
        if f.suffix in (".pcap", ".raw"):
            continue
        if f.stat().st_size > LIMIT:
            if f.name == "grade.json":
                g = json.loads(f.read_text())
                for k in ("segment_list", "joins", "rotation_run_list"):
                    g.pop(k, None)
                (dst / "grade-summary.json").write_text(json.dumps(g, indent=1) + "\n")
            continue
        shutil.copy2(f, dst / f.name)
dst = P / "runs" / "controller"
dst.mkdir(parents=True, exist_ok=True)
for f in sorted((RAW / "controller-staging").iterdir()):
    if f.suffix != ".py":
        shutil.copy2(f, dst / f.name)

# 3: redaction
orig_root = RAW / "packet-originals"
records = []
for d in ("identity", "restore", "soc", "runs", "summary", "gates"):
    for f in sorted((P / d).rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(P).as_posix()
        o = orig_root / rel
        data = o.read_bytes() if o.exists() else f.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("latin-1")
        new, labels = text, set()
        for r, b in LIT + RX:
            new, k = r.subn(b, new)
            if k:
                labels.add(b)
        if new != text:
            o.parent.mkdir(parents=True, exist_ok=True)
            if not o.exists():
                o.write_bytes(data)
            f.write_bytes(new.encode("utf-8"))
            records.append(dict(file=rel, original_sha256=sha(data), retained_sha256=sha(new.encode("utf-8")),
                                labels=sorted(labels)))
left = []
for d in ("identity", "restore", "soc", "runs", "summary", "gates", "tools"):
    for f in sorted((P / d).rglob("*")):
        if f.is_file():
            t = f.read_bytes().decode("utf-8", "replace")
            for c in m["check"]:
                if c.lower() in t.lower():
                    left.append((f.relative_to(P).as_posix(), "check-token"))
(P / "redaction.json").write_text(json.dumps(dict(
    rule=("Bench host names, interface names, the controller's, the reference peer's and the grandmaster's "
          "identifiers, the bridge network's addresses and MACs, home paths and the account name are replaced "
          "by the role labels listed per file. The DUT's entity, MAC and stream identifiers are public and "
          "retained. Each original stays under the raw root in packet-originals/, identified by its SHA-256."),
    files=records, residual_check_hits=len(left)), indent=1) + "\n")

# 4: raw index
idx = []
for f in sorted(RAW.rglob("*")):
    if f.is_file():
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        idx.append(dict(path=f.relative_to(RAW).as_posix(), bytes=f.stat().st_size, sha256=h.hexdigest()))
(P / "RAW-ARTIFACTS.json").write_text(json.dumps(dict(
    raw_root="/tmp/b3-a453/raw on the bench host (not published)", files=len(idx),
    total_bytes=sum(x["bytes"] for x in idx), entries=idx), indent=1) + "\n")
print(json.dumps(dict(redacted_files=len(records), residual_check_hits=left, raw_files=len(idx),
                      raw_bytes=sum(x["bytes"] for x in idx))))
