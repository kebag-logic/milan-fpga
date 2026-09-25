#!/usr/bin/env python3
"""R296-2 reviewer-owned mutants for the obj_crflic leg (PR #553 / issue #551).

Run from a DISPOSABLE parent clone's tb/verilator/milan_dp with the pinned
simulator first on PATH. Each mutant is planted in a temporary copy of
milan_datapath.sv, built through the leg's own recipe (make crflic-build with
DP_SRC and CRFLIC_MDIR overridden) and run. A mutant is CAUGHT only when the
leg itself reports failures; the failing check names are printed.

Usage: python3 reviewer_mutants.py <disposable-clone>/tb/verilator/milan_dp
"""

import subprocess
import sys
import tempfile
from pathlib import Path

GATE = ("  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
        "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];")
MUTANTS = [
    ("gate is ACTIVE OR real grant", GATE,
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] |\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];"),
    ("gate is ACTIVE AND a one-cycle-late grant", GATE,
     "  logic [SRP_TALKERS_C-1:0] r296_adm_q = '0;\n"
     "  always_ff @(posedge axis_clk) r296_adm_q <= pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];\n"
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
     "                             (pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0] | r296_adm_q);"),
]


def main() -> int:
    here = Path(sys.argv[1]).resolve()
    src = (here / "../../../hdl/milan/milan_datapath.sv").resolve().read_text()
    caught = 0
    with tempfile.TemporaryDirectory(prefix="r296-mut-", dir=str(here)) as td:
        work = Path(td)
        for name, pat, rep in MUTANTS:
            assert src.count(pat) == 1, name
            tag = name.replace(" ", "_")
            mpath = work / f"dp_{tag}.sv"
            mpath.write_text(src.replace(pat, rep))
            mdir = work / f"obj_{tag}"
            b = subprocess.run(["make", "-s", "-C", str(here), "crflic-build",
                                f"DP_SRC={mpath}", f"CRFLIC_MDIR={mdir}"],
                               capture_output=True, text=True, check=False)
            exe = mdir / "Vmilan_dp_crflic"
            if b.returncode != 0 or not exe.is_file():
                print(f"[NOT-EVIDENCE] {name}: build failed rc={b.returncode}")
                print(b.stdout[-1500:] + b.stderr[-1500:])
                continue
            r = subprocess.run([str(exe)], cwd=str(here), capture_output=True,
                               text=True, check=False)
            out = r.stdout + r.stderr
            fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
            tally = [ln for ln in out.splitlines() if ln.startswith("checks:")]
            if r.returncode != 0 and fails:
                caught += 1
                print(f"[CAUGHT] {name}: rc={r.returncode} {tally}")
            else:
                print(f"[SURVIVED] {name}: rc={r.returncode} {tally}")
            for ln in fails[:12]:
                print("    " + ln[:150])
    print(f"{caught}/{len(MUTANTS)} reviewer mutants caught")
    return 0 if caught == len(MUTANTS) else 1


if __name__ == "__main__":
    sys.exit(main())
