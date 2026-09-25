#!/usr/bin/env python3
"""[R312] round-3 text check: does SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18
and UNRESOLVED 6 state the corrected capture-hold premise, and does any tracked
document still hand the capture-hold measurement to the donor writer?

Usage: r3_text_check.py <repo root> <capture_copy_probe.log> <hold_margin.log>
Read-only. Prints one line per check; exit 1 if any REQUIRED check fails.
Residual donor-trigger hits are REPORTED (exit status unaffected) so the
reviewer grades them.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
probe = Path(sys.argv[2]).read_text()
margin = Path(sys.argv[3]).read_text()
page = (root / "docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md").read_text().splitlines()


def section(start_re, end_re):
    s = next(i for i, l in enumerate(page) if re.match(start_re, l))
    e = next(i for i in range(s + 1, len(page)) if re.match(end_re, page[i]))
    return s + 1, "\n".join(page[s:e])


s18_line, s18 = section(r"^## 18\. ", r"^## 19\. ")
u_line, u20 = section(r"^## 20\. ", r"^## 21\. ")
u6_start = u20.index("\n6. ")
u6 = u20[u6_start:u20.index("\n7. ")]
print(f"section 18 starts at line {s18_line}; section 20 at line {u_line}")

m = re.search(r"endstation_ax7101_8x8: capture copied (\d+) bytes over (\d+) records "
              r"\((\d+) bytes in ids", probe)
bytes8, recs8, mapo8 = (int(x) for x in m.groups())
m1 = re.search(r"endstation_ax7101_1x1_tdm8: capture copied (\d+) bytes over (\d+) records", probe)
bytes1, recs1 = (int(x) for x in m1.groups())
assert "copy=63.8 ms margin_to_50ms=0.78x" in margin and "copy=31.9 ms margin_to_50ms=1.57x" in margin


def fmt(n):
    return f"{n:,}"


REQ = [
    ("s18 CLOSED-record copy by nvm_capture", s18, r"`nvm_capture\(\)` copies every CLOSED record at each capture"),
    ("s18 independent of materialization", s18, r"Materialization does not affect that copy"),
    ("s18 RELOAD closes every allocated record", s18, r"accepted RELOAD closes every allocated record"),
    ("s18 counted 8x8 bytes/records", s18, re.escape(f"{fmt(bytes8)} bytes over {recs8} records")),
    ("s18 output-map bytes", s18, re.escape(f"{fmt(mapo8)} of those bytes")),
    ("s18 exposure at this head", s18, r"exposure therefore exists at this head"),
    ("s18 table 8x8 nominal", s18, r"31\.9 ms / 1\.57x"),
    ("s18 table 8x8 doubled", s18, r"63\.8 ms / 0\.78x"),
    ("s18 table 1x1 raw", s18, re.escape(f"{fmt(bytes1)} / {recs1}")),
    ("s18 table 1x1 margins", s18, r"8\.3 ms / 6\.06x.*\n.*16\.5 ms / 3\.03x"),
    ("s18 safety void/retry", s18, r"voids capture; release and retry preserve safety"),
    ("s18 1x1 unchanged", s18, r"shipping 1x1 shape and its margins are unchanged"),
    ("s18 cites #559", s18, r"issues/559\)"),
    ("s18 cites corrected decision 5824117439", s18, r"issuecomment-5824117439"),
    ("u6 CLOSED-record copy", u6, r"`nvm_capture\(\)` copies every CLOSED record at each capture"),
    ("u6 independent of materialization", u6, r"Materialization does not affect that copy"),
    ("u6 counted 8x8 bytes", u6, re.escape(f"{fmt(bytes8)} bytes over {recs8} records")),
    ("u6 output-map bytes", u6, re.escape(f"{fmt(mapo8)} output-map bytes within those {fmt(bytes8)} bytes")),
    ("u6 margins 8x8", u6, r"1\.57x and 0\.78x"),
    ("u6 0.78x at this head", u6, r"0\.78x modelled margin applies at this head"),
    ("u6 safety", u6, r"Void and retry preserve safety"),
    ("u6 1x1 unchanged", u6, r"1x1 stays unchanged: 8\.3/16\.5 ms, margins 6\.06x/3\.03x"),
    ("u6 cites #559", u6, r"issues/559\)"),
]
FORBID = [
    r"maps are not copied", r"No materialized map copy", r"Only BINDING is materialized today",
    r"issuecomment-5823590638", r"issuecomment-5823589125", r"#61/#83 adoption must measure",
    r"Donor writer adoption",
]
fail = 0
for name, text, pat in REQ:
    ok = re.search(pat, text) is not None
    fail |= not ok
    print(f"{'PASS' if ok else 'FAIL'} required: {name}")
for pat in FORBID:
    for name, text in (("section 18", s18), ("UNRESOLVED 6", u6)):
        hit = re.search(pat, text) is not None
        fail |= hit
        print(f"{'FAIL' if hit else 'PASS'} absent in {name}: {pat!r}")

# Repository-wide residue: any tracked Markdown tying the donor to the
# capture-hold measurement, or linking the withdrawn obligation.
RESIDUE = re.compile(r"capture-hold measurement obligation|issuecomment-5823590638|"
                     r"donor obligation|donor acceptance obligation", re.I)
for md in sorted(root.glob("docs/**/*.md")):
    lines = md.read_text().splitlines()
    for i, l in enumerate(lines):
        if RESIDUE.search(l):
            ctx = " ".join(x.strip() for x in lines[max(0, i - 1):i + 1])
            print(f"RESIDUE {md.relative_to(root)}:{i + 1}: {ctx}")
print("required checks:", "FAIL" if fail else "all PASS")
sys.exit(1 if fail else 0)
