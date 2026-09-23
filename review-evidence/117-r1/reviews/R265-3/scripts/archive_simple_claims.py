#!/usr/bin/env python3
"""Re-derive simple countable page claims from the pinned evidence archive.

Usage: archive_simple_claims.py <evidence-root: .../review-evidence/117-r1>

1. Tap records without a valid 28-octet envelope, per tap capture.
2. tcpdump logs: count and "dropped by kernel" figures.
3. Console transcripts: count, and the command census by verb.
4. Host daemon check lines (gPTP/AVB daemons) in the A200 host record.
5. Binding census stream_dest_mac difference (A200 start vs final).
"""
import collections
import glob
import json
import os
import re
import struct
import sys


def pcap_records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    assert magic in (0xA1B2C3D4, 0xA1B23C4D), path
    off = 24
    while off + 16 <= len(raw):
        _, _, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        yield raw[off:off + incl]
        off += incl


def main():
    root = sys.argv[1]
    print("== 1. tap captures: records without a valid envelope (tag 6, port 2/3)")
    for p in sorted(glob.glob(os.path.join(root, "**", "*.pcap"), recursive=True)):
        rel = os.path.relpath(p, root)
        n = bad = 0
        for pkt in pcap_records(p):
            n += 1
            if len(pkt) < 42:
                bad += 1
                continue
            tag, _, port = struct.unpack("<III", pkt[:12])
            if tag != 6 or port not in (2, 3):
                bad += 1
        kind = "tap" if (os.path.basename(p).startswith("tap") or "probe-tap" in p) else "non-tap"
        print(f"   {kind:7s} {rel:55s} records {n:7d} no-envelope {bad}")

    print("== 2. tcpdump logs")
    logs = sorted(glob.glob(os.path.join(root, "**", "tcpdump*.log"), recursive=True))
    print("   logs:", len(logs))
    for p in logs:
        t = open(p, errors="replace").read()
        m = re.findall(r"(\d+) packets? dropped by kernel", t)
        c = re.findall(r"(\d+) packets? captured", t)
        print(f"   {os.path.relpath(p, root):55s} captured {c} dropped-by-kernel {m}")

    print("== 3. console transcripts")
    cons = []
    for p in sorted(glob.glob(os.path.join(root, "**", "*.txt"), recursive=True)):
        t = open(p, errors="replace").read()
        if re.search(r"^### \S+ cmd='", t, re.M):
            cons.append((p, t))
    print("   transcripts with command headers:", len(cons))
    total = collections.Counter()
    for p, t in cons:
        verbs = collections.Counter(c.split()[0] if c.split() else "" for c in re.findall(r"^### \S+ cmd='([^']*)'", t, re.M))
        total.update(verbs)
        print(f"   {os.path.relpath(p, root):55s} {sum(verbs.values()):6d} {dict(verbs)}")
    print("   total commands:", sum(total.values()), dict(total))

    print("== 4. A200 host daemon record (lines naming a time daemon)")
    hp = os.path.join(root, "bench-a200", "bench", "hosts-clock-and-daemons.txt")
    for line in open(hp, errors="replace"):
        if re.search(r"ptp4l|phc2sys|gptp|avdecc|daemon|systemd-timesyncd|chrony|ntp|process|pgrep|ps ", line, re.I):
            print("   |", line.rstrip()[:160])

    print("== 5. A200 binding census start vs final: fields that differ")
    def load(p):
        rows = []
        for line in open(p):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return rows
    a = load(os.path.join(root, "bench-a200", "bench", "census-start.jsonl"))
    b = load(os.path.join(root, "bench-a200", "bench", "final", "census-final.jsonl"))
    print("   rows start", len(a), "final", len(b))
    def flat(o, pre=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from flat(v, f"{pre}.{k}" if pre else k)
        else:
            yield pre, o
    ka = {}
    for r in a:
        key = (r.get("cmd") or r.get("what"), r.get("target"), json.dumps(r.get("index", r.get("stream_index")), sort_keys=True))
        ka[key] = dict(flat(r.get("decoded", r)))
    diffs = collections.Counter()
    for r in b:
        key = (r.get("cmd") or r.get("what"), r.get("target"), json.dumps(r.get("index", r.get("stream_index")), sort_keys=True))
        if key in ka:
            fb = dict(flat(r.get("decoded", r)))
            for k in set(fb) | set(ka[key]):
                if k in ("t", "seq", "rtt_ms") or k.endswith(".t"):
                    continue
                if fb.get(k) != ka[key].get(k):
                    diffs[(key[0], k)] += 1
    for (cmd, k), n in sorted(diffs.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        print(f"   differs: {cmd} field {k} x{n}")


if __name__ == "__main__":
    main()
