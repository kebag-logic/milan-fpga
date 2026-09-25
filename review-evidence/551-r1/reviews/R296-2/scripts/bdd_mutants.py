#!/usr/bin/env python3
"""R296-2: plant gate-expression mutants in a DISPOSABLE parent clone and run
the specification-facing licence feature against each; restore after each.

Usage: python3 bdd_mutants.py <disposable-clone>
Exit 0 when the clean control passes and every mutant fails the feature.
"""

import subprocess
import sys
from pathlib import Path

GATE = ("  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
        "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];")
MUTANTS = [
    ("ACTIVE only", "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0];"),
    ("raw grant only", "  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];"),
    ("ACTIVE OR grant", GATE.replace("] &\n", "] |\n")),
    ("ACTIVE AND grant AND extra term", GATE[:-1] + " & {SRP_TALKERS_C{1'b1}};"),
]


def behave(tests: Path) -> tuple[int, str]:
    r = subprocess.run(["behave", "--no-capture", "-f", "plain",
                        "features/milan_streaming_licence.feature"],
                       cwd=str(tests), capture_output=True, text=True, check=False)
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    dp = root / "hdl/milan/milan_datapath.sv"
    tests = root / "tests"
    orig = dp.read_text()
    assert orig.count(GATE) == 1
    ok = True
    try:
        rc, out = behave(tests)
        print(f"[control] clean rc={rc}")
        ok &= rc == 0
        for name, rep in MUTANTS:
            dp.write_text(orig.replace(GATE, rep))
            rc, out = behave(tests)
            failed = [ln.strip() for ln in out.splitlines() if "failed" in ln and "Then" in ln]
            print(f"[{'CAUGHT' if rc != 0 else 'SURVIVED'}] {name}: rc={rc}")
            for ln in failed[:3]:
                print("    " + ln[:160])
            ok &= rc != 0
    finally:
        dp.write_text(orig)
    rc, _ = behave(tests)
    print(f"[control] restored rc={rc}")
    ok &= rc == 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
