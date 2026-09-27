#!/usr/bin/env python3
"""Disposable P4 probe: drop the phase-5 term from amap_edit_live_wr_p.

Usage: p4_probe.py <repo> <scratch-dir>

Copies milan_datapath.sv into <scratch-dir>, removes the
`(pp_amap_edit_phase_w == 3'd5) &&` term from the actual-write predicate,
and runs `make run-pending` of tb/verilator/pp_shadow with the mutant in
place of the shipping file (the same substitution pending_mutant.py uses).
The shipping source is never written. Exit 0 when the mutant fails and the
failures include the case-tagged partial-refusal sticky checks.
"""
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    here = repo / "tb/verilator/pp_shadow"
    source = repo / "hdl/milan/milan_datapath.sv"
    original = source.read_text()
    anchor = ("      && (pp_amap_edit_phase_w == 3'd5) && amap_edit_context_w\n")
    if original.count(anchor) != 1:
        print("REFUSED: P4 anchor not found exactly once")
        return 2
    mutant = scratch / "p4/hdl/milan/milan_datapath.sv"
    mutant.parent.mkdir(parents=True, exist_ok=True)
    mutant.write_text(original.replace(anchor, "      && amap_edit_context_w\n"))
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"],
                             cwd=here, check=True, capture_output=True,
                             text=True).stdout.split()
    sources = [(here / p).resolve() for p in listing]
    if sources.count(source) != 1:
        print("REFUSED: expected exactly one shipping datapath")
        return 2
    sources = [mutant if p == source else p for p in sources]
    log = scratch / "p4/run.log"
    with log.open("w") as out:
        rc = subprocess.run(["make", "run-pending",
                             f"PENDING_BUILD_DIR={scratch / 'p4/obj'}",
                             "DP_SRCS=" + " ".join(map(str, sources))],
                            cwd=here, stdout=out, stderr=subprocess.STDOUT
                            ).returncode
    text = log.read_text()
    if source.read_text() != original:
        print("FAIL: shipping source changed")
        return 3
    fails = [l.strip() for l in text.splitlines() if "[FAIL]" in l]
    for line in text.splitlines():
        if "checks," in line or line.startswith("RESULT"):
            print(line)
    print("\n".join(fails))
    need = ("K12 partial refusal input sticky_pending_PP_STAT",
            "K12 partial refusal output sticky_pending_PP_STAT")
    killed = rc != 0 and all(any(n in f for f in fails) for n in need)
    print(f"make rc={rc}; P4 {'KILLED' if killed else 'NOT KILLED'} "
          f"by the tagged partial-refusal checks")
    return 0 if killed else 1


if __name__ == "__main__":
    sys.exit(main())
