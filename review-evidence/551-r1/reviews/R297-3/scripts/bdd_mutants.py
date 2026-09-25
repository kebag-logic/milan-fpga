#!/usr/bin/env python3
"""R297-3 reviewer-owned BDD mutation runner for the #551 stream-gate scenario.

Extracts `git archive HEAD` of the repository (tracked files at the exact
head, no submodules) into a disposable directory per arm, rewrites the lwsrp_stream_gate assignment there (never
in the clone), and runs the milan_streaming_licence feature. The clean copy
must pass before and after; each mutant must fail (behave rc != 0).

Usage: bdd_mutants.py <repo> <scratch-dir> <receipt-dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO, SCRATCH, OUT = (Path(p).resolve() for p in sys.argv[1:4])
ORIG = ("assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
        "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];")
A = "pp_cd_srp_active_w[SRP_TALKERS_C-1:0]"
G = "pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0]"
ARMS = [
    ("clean_before", None, 0),
    ("active_only", "assign lwsrp_stream_gate = %s;" % A, 1),
    ("grant_only", "assign lwsrp_stream_gate = %s;" % G, 1),
    ("active_or_grant", "assign lwsrp_stream_gate = %s | %s;" % (A, G), 1),
    ("extra_term", "assign lwsrp_stream_gate = %s & %s & {SRP_TALKERS_C{cfg_lwsrp_enable}};" % (A, G), 1),
    ("clean_after", None, 0),
]


def run(name, text):
    root = SCRATCH / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD"],
                         capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=arc, check=True)
    dp = root / "hdl" / "milan" / "milan_datapath.sv"
    src = dp.read_text(encoding="utf-8")
    assert src.count(ORIG) == 1, "gate assignment not found exactly once"
    if text is not None:
        src = src.replace(ORIG, text)
    dp.write_text(src, encoding="utf-8")
    p = subprocess.run(
        ["behave", "--no-capture", "-f", "plain", "features/milan_streaming_licence.feature"],
        cwd=root / "tests", capture_output=True, text=True)
    (OUT / ("bdd_%s.log" % name)).write_text(
        "arm: %s\nmutation: %s\nrc: %d\n--- stdout\n%s--- stderr\n%s" %
        (name, text, p.returncode, p.stdout, p.stderr), encoding="utf-8")
    return p.returncode


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines, ok = [], True
    for name, text, want_fail in ARMS:
        rc = run(name, text)
        good = (rc != 0) if want_fail else (rc == 0)
        ok &= good
        lines.append("%-16s rc=%d expect=%s %s" % (
            name, rc, "FAIL" if want_fail else "PASS", "OK" if good else "WRONG"))
    lines.append("overall: %s" % ("OK" if ok else "WRONG"))
    (OUT / "bdd_mutants_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
