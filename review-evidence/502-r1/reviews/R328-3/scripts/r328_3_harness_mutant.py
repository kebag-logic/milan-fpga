#!/usr/bin/env python3
"""R328-3 harness sanity mutant for the committed K12 partial-refusal control.

Usage: r328_3_harness_mutant.py <disposable-tree> <outdir>

Derives tb/verilator/pp_shadow/r328_3_nocf_main.cpp in the DISPOSABLE tree
from the head's sim_main.cpp, deleting only the line that makes record 1
conflict with record 0's claim (so the two records are identical), and runs
the dynamic-output leg with CPP=. The control must then FAIL on its status,
map-count and pending/storage grading: evidence those checks can fail.
No reviewed file is edited.
"""
import subprocess
import sys
from pathlib import Path

LINE = "        put16be(partial.data() + (type == 0xe ? 18 : 20), 1);\n"


def main():
    tree = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    tb = tree / "tb/verilator/pp_shadow"
    src = (tb / "sim_main.cpp").read_text()
    if src.count(LINE) != 1:
        sys.exit("REFUSED: anchor count %d" % src.count(LINE))
    (tb / "r328_3_nocf_main.cpp").write_text(src.replace(LINE, ""))
    out.mkdir(parents=True, exist_ok=True)
    log = out / "no_conflict.log"
    with log.open("w") as fh:
        rc = subprocess.run(["make", "run-pending", f"PENDING_BUILD_DIR={out / 'build'}",
                             "CPP=r328_3_nocf_main.cpp"], cwd=tb, stdout=fh,
                            stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    fails = sorted({l.split("got=")[0].strip() for l in text.splitlines() if "[FAIL]" in l})
    print("\n".join(fails))
    print([l for l in text.splitlines() if l.startswith(("pp_shadow:", "RESULT"))])
    print(f"rc={rc} verdict={'KILLED' if 'RESULT: FAIL' in text else 'SURVIVED' if 'RESULT: PASS' in text else 'BUILD-FAIL'}")


if __name__ == "__main__":
    main()
