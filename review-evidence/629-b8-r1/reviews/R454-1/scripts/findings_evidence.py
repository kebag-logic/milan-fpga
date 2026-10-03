#!/usr/bin/env python3
"""Reproduce the evidence behind R454-1's findings from the page and the published packet.

usage: findings_evidence.py <page.md> <packet author dir>

Value-blind where the finding is about a private value: it prints line numbers,
a classification and hashes, never the private value itself.
"""
import hashlib
import json
import pathlib
import re
import sys

page, pkt = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = page.read_text().splitlines()

print("== F1: the external capture's channel count as a literal in a published tool")
g = (pkt / "tools/grade_b8.py").read_text().splitlines()
for n, line in enumerate(g, 1):
    if re.search(r"which of the \d+ capture channels", line):
        print(f"tools/grade_b8.py:{n}: a literal channel count in the channel-identification docstring "
              f"(line sha256 {hashlib.sha256(line.encode()).hexdigest()[:16]})")
red = json.loads((pkt / "redaction.json").read_text())["files"]
print("grade_b8.py listed in redaction.json:", "tools/grade_b8.py" in red)
print("page row for tools/grade_b8.py marked masked:",
      any("tools/grade_b8.py" in l and "masked" in l for l in text))

print("== F2: the external capture's sample layout readable from published tool code")
for tool in ("tools/run_b8.py", "tools/grade_b8.py"):
    for n, line in enumerate((pkt / tool).read_text().splitlines(), 1):
        if re.search(r"reshape\(n, (NCH|nch), \d\)|NCH \* \d|\(\d \* nch\)|<< 16\)", line):
            print(f"{tool}:{n}: per-sample byte width or byte-order decode of the capture")
for n, line in enumerate(text, 1):
    if "at one line that would state" in line:
        print(f"page:{n}: {line.strip()}")

print("== F3: the CRF window's capture loss and stall-cluster signature")
gr = json.loads((pkt / "summary/crfll/grade.json").read_text())
ev = [json.loads(l) for l in (pkt / "runs/crfll/events.jsonl").open()]
t0 = next(e["t"] for e in ev if e["kind"] == "window-start")
t1 = next(e["t"] for e in ev if e["kind"] == "window-end")
lost = gr["frame_rate_ratio"]["counted"]["capture_lost_frames"]
obs = gr["window"]["frames"]
print(f"window by events: {t1 - t0:.3f} s; captured {obs} frames = {obs / 48000:.2f} s; "
      f"capture-path lost {lost} frames = {lost / 48000:.2f} s")
stalls = [c for c in gr["skip_clusters"] if c["lost_ms"] > 1000]
print("stall clusters:", [(c["cluster"], round(c["lost_ms"] / 1e3, 2), c["size_signature"], c["steps"][-2:])
                          for c in stalls])
print(f"stall clusters lost {sum(c['lost_frames'] for c in stalls) / 48000:.2f} s")
for n, line in enumerate(text, 1):
    if "19.0 s" in line or "off the" in line and "signature" in line:
        print(f"page:{n}: {line.strip()}")

print("== F4: where the B8 packet is published")
sec = "\n".join(text[[i for i, l in enumerate(text) if l.startswith("### B8: artifact hashes")][0]:])
print("B8 hashes section names a published branch or pin:",
      bool(re.search(r"review-evidence|published on branch|pinned at", sec)))

print("== R1: SLIP_TDM address label")
for n, line in enumerate(text, 1):
    if "`SLIP_TDM`, the TDM junction's" in line or (n > 1 and "`SLIP_TDM`, the TDM junction's" in text[n - 2]):
        print(f"page:{n}: {line.strip()}")

print("== R2: raw-hash provenance")
pe = (pkt / "runs/proof/events.jsonl").read_text()
print("proof events.jsonl carries the recording's sha256:", "b1dc772d8fcb" in pe)
