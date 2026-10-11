#!/usr/bin/env python3
"""R598-1 reviewer mutation probe for the CSR read-path lockstep (PR #722).

Independent of the lane's lock_mutants.py: each mutant below is written by the
reviewer, planted into a copy of hdl/common/csr/milan_csr.sv from a disposable
tree, built through that tree's own Makefile (lock1 / lock8 with LOCK_SRC and
the leg's MDIR overridden) and run. A mutant counts as KILLED only when the
harness exits non-zero AND prints `[FAIL] <expected check>`.

usage: r598_mutants.py <tree> <workdir> <jobs> [name ...]
"""
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

# (name, old text (must occur exactly once), new text, expected check, leg)
MUTANTS = [
    # --- two of the lane's classes, re-applied in a different form ---
    ("R-decode-ptp-hi", "      A_PTP_TRHI:   live_mux = ptp_tod_rd[63:32];",
     "      A_PTP_TRHI:   live_mux = ptp_tod_rd[31:0];", "decode", "lock1"),
    ("R-torn-pdus", "        A_STRMW_PDUS:  strm_mux = snap_shadow_r[11];",
     "        A_STRMW_PDUS:  strm_mux = i_pcmrx_cnt;", "snapshot-coherence", "lock1"),
    # --- reviewer-chosen defects in the lane's own change ---
    ("N-shadow-or-live", "  wire shadow_rd_w = rd_in_window && !live_hit;",
     "  wire shadow_rd_w = rd_in_window;", "decode", "lock1"),
    ("N-talker-idx0-raw",
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_POISON_C;\n"
     "              snap_shadow_r[11] <= i_aaf_frames;",
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_RAW_C;\n"
     "              snap_shadow_r[11] <= i_aaf_frames;", "snapshot-coherence", "lock1"),
    ("N-oor-kind-kept",
     "            for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_ZERO_C;\n",
     "", "snapshot-freshness", "lock1"),
    ("N-kind-index-off-by-one",
     "            unique case (snap_kind_r[1 + 32'(coff[5:2])])",
     "            unique case (snap_kind_r[32'(coff[5:2])])", "decode", "lock1"),
    ("N-burst-gate-wrong", "              default: if (N_LISTENERS_P > 1) begin",
     "              default: if (N_LISTENERS_P > 8) begin", "snapshot-coherence", "lock8"),
    ("N-poison-word", "              SK_POISON_C: strm_mux = 32'hDEAD_DEAD;",
     "              SK_POISON_C: strm_mux = 32'hDEAD_BEEF;", "snapshot-coherence", "lock1"),
    ("N-stage1-gate-window-only",
     "        live_mux_q <= (strm_hit || rd_in_window) ? live_mux : 32'h0;",
     "        live_mux_q <= rd_in_window ? live_mux : 32'h0;", "decode", "lock1"),
    ("N-extra-talker-kind-raw",
     "            if (strm_dir_r)\n"
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_POISON_C;",
     "            if (strm_dir_r)\n"
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_RAW_C;",
     "snapshot-coherence", "lock8"),
    # equivalence probe: dropping the stage-1 window gate entirely. Expected to
    # SURVIVE today (every live arm >= 0x800 is in rd_in_window); recorded as a
    # characterisation, not as a test-strength claim.
    ("E-stage1-gate-dropped",
     "        live_mux_q <= (strm_hit || rd_in_window) ? live_mux : 32'h0;",
     "        live_mux_q <= live_mux;", None, "lock1"),
]


def one(tree: Path, work: Path, m) -> str:
    name, old, new, check, leg = m
    src = (tree / "hdl/common/csr/milan_csr.sv").read_text()
    if src.count(old) != 1:
        return f"{name}: PATTERN-COUNT {src.count(old)} (not applied)"
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    rtl = d / "milan_csr.sv"
    rtl.write_text(src.replace(old, new))
    b = subprocess.run(["make", "-s", "-C", str(tree / "tb/verilator/csr"), leg,
                        f"LOCK_SRC={rtl}", f"{leg.upper()}_MDIR={d / 'obj'}"],
                       capture_output=True, text=True, check=False)
    (d / "build.log").write_text(b.stdout + b.stderr)
    exe = d / "obj" / "Vcsr_lock"
    if b.returncode != 0 or not exe.is_file():
        return f"{name}: BUILD-FAILED rc={b.returncode}"
    r = subprocess.run([str(exe)], cwd=str(tree / "tb/verilator/csr"),
                       capture_output=True, text=True, check=False)
    (d / "run.log").write_text(r.stdout + r.stderr)
    fails = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("[FAIL]")]
    names = [f[len("[FAIL]"):].split(":")[0].strip() for f in fails]
    if check is None:
        verdict = "SURVIVED (equivalence probe)" if r.returncode == 0 and not fails \
            else "KILLED (equivalence probe expected survival)"
    elif r.returncode != 0 and check in names:
        verdict = f"KILLED by {check}"
    elif r.returncode == 0 and not fails:
        verdict = "SURVIVED"
    else:
        verdict = f"FAILED OTHERWISE rc={r.returncode} checks={names}"
    return f"{name} [{leg}]: {verdict}; failed={names}"


def main() -> int:
    tree, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
    sel = [m for m in MUTANTS if len(sys.argv) < 5 or m[0] in sys.argv[4:]]
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        results = list(ex.map(lambda m: one(tree, work, m), sel))
    for line in results:
        print(line)
    bad = [r for r in results if not ("KILLED by" in r or "SURVIVED (equivalence probe)" in r)]
    print(f"{len(results)} mutants, {len(results) - len(bad)} as expected, {len(bad)} not")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
