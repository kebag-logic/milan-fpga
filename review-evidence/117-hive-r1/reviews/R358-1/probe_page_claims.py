#!/usr/bin/env python3
"""R358-1 probe: every hash and number the PR adds to the findings page, checked
against the raw packet (author MANIFEST.sha256 = recorded bytes; publisher
MANIFEST.json = published bytes).

usage: probe_page_claims.py <repo_root> <packet_dir> <head>
"""
import json
import re
import subprocess
import sys
from pathlib import Path

root, packet, head = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
page = subprocess.run(["git", "show", f"{head}:docs/findings/117_GPTP_SILICON_EVIDENCE.md"], cwd=root,
                      capture_output=True, text=True, check=True).stdout
a = packet / "author"
recorded = dict(reversed(l.split()) for l in (a / "MANIFEST.sha256").read_text().splitlines())
published = {e["file"].removeprefix("author/"): e for e in json.loads((packet / "MANIFEST.json").read_text())}
fails = []


def check(cond, msg):
    print(("OK   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


# B4 artifact table
b4 = page[page.index("| B4 artifact in packet |"):page.index("## Raw artifacts")]
rows = re.findall(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$", b4, re.M)
check(len(rows) == 10, f"B4 artifact table has 10 rows (found {len(rows)})")
for name, h in rows:
    same_pub = published[name]["published_sha256"] == h
    check(recorded.get(name) == h, f"{name}: page hash equals recorded (author manifest) hash"
          + ("; published copy identical" if same_pub else "; PUBLISHED COPY DIFFERS (publisher-redacted)"))

exp = (a / "expected-crc.txt").read_text()
uart = (a / "identity-uart.txt").read_text()
prov = (a / "build-provenance.txt").read_text()
summ = [json.loads(l) for l in (a / "enumeration-summary.txt").read_text().splitlines() if l.startswith("{")]
for label, size, h in (("bitfile", "3825992", "1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7"),
                       ("bitpay", "3825788", "bcae1666501422d82397df9abccf6a1d1736714ae7b482920a345d91b58b4db3"),
                       ("aem", "7352", "9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404")):
    check(re.search(rf"{label}\s+len=\s*{size} crc32=\w+ sha256={h}", exp) is not None and h in page,
          f"{label} size/hash on page equal expected-crc.txt")
for v in ("VERSION=00020060", "CRC32: 9b6576a9", "CRC32: 3c18c276", "CRC32: 93742dd2", "crc 0x00000000 52216"):
    check(v in uart, f"UART transcript contains {v}")
check("changed_offsets=[]" in (a / "identity-aecp-comparison.txt").read_text(), "AECP comparison: no changed offsets")
check("6d61a92e7f264c69f23cdc38f50d31114e567aa0" in prov and "v4.3.1.1" in prov and "16.1.1" in prov,
      "library revision, tag and compiler version in build-provenance.txt")
check("ac552f67c8b769e0cfc46d0b80c4e9ece0c9da1811020d2c497e2f904749a623" == recorded["tools/enum_probe.cpp"]
      and "ac552f67c8b769e0cfc46d0b80c4e9ece0c9da1811020d2c497e2f904749a623" in page, "probe source hash")
for d in ("ENABLE_AVDECC_FEATURE_REDUNDANCY", "ENABLE_AVDECC_FEATURE_JSON", "ENABLE_AVDECC_FEATURE_CBR",
          "ENABLE_AVDECC_STRICT_2018_REDUNDANCY", "-std=c++17", "-O2", "-Wall"):
    check(d in prov, f"build flag {d} recorded")
page_windows = {1: ("17:29:27", "17:29:39", 234), 2: ("17:30:03", "17:30:15", 229), 3: ("17:30:23", "17:30:35", 169)}
for s in summ:
    n = s["run"]
    st, en, t = page_windows[n]
    check(st in s["window"][0] and en in s["window"][1] and s["window"][1].endswith("rc=0")
          and s["statistics"]["enumeration_time"] == t and s["statistics"]["aecp_response_average_time"] == 3,
          f"run {n}: window, rc, enumeration time and 3 ms average as on page")
    check(f"| {n} | {st} to {en} | {t} ms | `IEEE17221`, `MILAN` | 0 / 0 / 0 |" in page, f"run {n} page row text")
check("460b15ac38dc05adac991bbd7f23f48640ee589703ae8d15b5eea4e5c4f0ec3b" in page
      and all(s["static_tree_sha256"] == "460b15ac38dc05adac991bbd7f23f48640ee589703ae8d15b5eea4e5c4f0ec3b" for s in summ),
      "canonical static tree hash equal on page and all three runs")
print("RESULT", "FAIL" if fails else "PASS", len(fails))
