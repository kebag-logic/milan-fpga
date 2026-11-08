#!/usr/bin/env python3
"""Freshness-gate plants for the register reference at one exact head.

Usage: python3 -I plants.py <clean-source-clone> <scratch-dir> <receipt-dir>
Each plant runs in its own shared clone of the source clone at its HEAD, applies
one edit, runs `scripts/gen_register_reference.py --check` and records the exit
status, the output and the diff. The generator needs the pinned wavedrom package
on the python3 found first on PATH.
"""
import re
import subprocess
import sys
from pathlib import Path

SRC, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:4])
RTL = "hdl/common/csr/milan_csr.sv"
PAGE = "docs/reference/REGISTER_MAP.md"


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, **kw)


def replace(root, rel, old, new, count):
    p = root / rel
    text = p.read_text()
    found = text.count(old)
    assert found == count, f"{rel}: {old!r} found {found} times, want {count}"
    p.write_text(text.replace(old, new))


def replace_word(root, rel, old, new, count):
    p = root / rel
    text, found = re.subn(rf"(?<![\w]){re.escape(old)}(?![\w])", new, p.read_text())
    assert found == count, f"{rel}: word {old!r} found {found} times, want {count}"
    p.write_text(text)


def dev_page(root):
    page = sh(["git", "show", "0a75aa774b89ac89351700f63dd8cbb89694af6c:" + PAGE], root).stdout
    (root / PAGE).write_text(page)


PLANTS = [
    ("p0_control", None, 0, "fresh"),
    ("p1_dev_handwritten_page", dev_page, 1, f"STALE {PAGE}"),
    ("p2_mac_ifg_reset_flop_and_rom", lambda r: (
        replace(r, RTL, "mac_ifg <= 32'h0C;", "mac_ifg <= 32'h0D;", 1),
        replace(r, RTL, "A_MAC_IFG[10:0]:    csr_default = 32'h0C;",
                "A_MAC_IFG[10:0]:    csr_default = 32'h0D;", 1)), 1, "STALE"),
    ("p3_field_signal_rename", lambda r: replace_word(r, RTL, "mac_ifg", "mac_gap", 4), 1,
     "STALE docs/diagrams/regmap/rtl_fingerprint.txt"),
    ("p4_register_rename", lambda r: replace(r, RTL, "A_ETH_GUARD", "A_ETH_LOCK", 3), 2,
     "needs a name and a purpose"),
    ("p5_comment_only", lambda r: replace(r, RTL, "//! [0] guarded (RW via magic)",
                                          "//! [0] fenced (RW via magic)", 1), 0, "fresh"),
    # Beyond the author's set: a description-only edit to the prose source must also go stale.
    ("p6_description_prose_edit", lambda r: replace(
        r, "scripts/register_descriptions.json", "Station MAC address bits 31 to 0",
        "Station MAC address bits 31 down to 0", 1), 1, f"STALE {PAGE}"),
]

failures = 0
OUT.mkdir(parents=True, exist_ok=True)
head = sh(["git", "rev-parse", "HEAD"], SRC).stdout.strip()
for name, plant, want_rc, want_text in PLANTS:
    root = SCRATCH / name
    sh(["rm", "-rf", str(root)], SCRATCH)
    sh(["git", "clone", "-q", "--shared", str(SRC), str(root)], SCRATCH)
    sh(["git", "checkout", "-q", "--detach", head], root)
    if plant:
        plant(root)
    diff = sh(["git", "diff", "--stat"], root).stdout
    res = sh(["python3", "scripts/gen_register_reference.py", "--check"], root)
    out = res.stdout + res.stderr
    ok = res.returncode == want_rc and want_text in out
    failures += not ok
    (OUT / f"{name}.log").write_text(f"# head {head}\n# want rc {want_rc}, text {want_text!r}\n"
                                     f"# diff:\n{diff}\n# rc {res.returncode}\n{out}")
    print(f"{'ok  ' if ok else 'FAIL'} {name}: rc {res.returncode} (want {want_rc}) "
          f"{' '.join(out.split())[:160]}")
print(f"plants: {len(PLANTS) - failures}/{len(PLANTS)} as expected")
sys.exit(1 if failures else 0)
