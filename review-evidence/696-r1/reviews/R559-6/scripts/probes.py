#!/usr/bin/env python3
"""Reviewer fault probes on KL_maap (unit harness). Usage:
probes.py <repo-root> <work-dir> <jobs>. Each probe is an exact single-anchor
replacement on a scratch copy of KL_maap.sv; a probe is CAUGHT only when the
build succeeds and the harness exits 1 with at least one [FAIL] line."""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
root, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
rtl = (root / "hdl/ieee1722/maap/KL_maap.sv").read_text()
PROBES = [
 ("q1_probe_fold_unstepped", "{10'd0, probe_fold(lfsr_next_w)}", "{10'd0, probe_fold(lfsr_r)}"),
 ("q2_offset_fold_unstepped", "offset_fold(seed_next_w), count_i)", "offset_fold(enable_seed_w), count_i)"),
 ("q3_offset_row0_bit_drop", "32'h1040_0000, 32'h0000_0081", "32'h1040_0000, 32'h0000_0080"),
 ("q4_reseed_every_begin", "if (enable_i && !rng_seeded_r) begin", "if (enable_i && state_r == IDLE_S) begin"),
 ("q5_every_begin_first_fold", "rand_offset(rng_seeded_r ? lfsr_next_w[15:0]", "rand_offset(1'b0 ? lfsr_next_w[15:0]"),
 ("q6_no_zero_fallback", "(mac_seed_w == 32'h0) ? 32'hACE1 : mac_seed_w", "mac_seed_w"),
 ("q7_probe_fold_row_drop", "32'h0000_0409, 32'h2420_0880", "32'h0000_0409, 32'h0000_0000"),
 ("q8_first_offset_count8", "offset_fold(seed_next_w), count_i)", "offset_fold(seed_next_w), 8'd8)"),
]
def run(p):
    name, a, b = p
    if rtl.count(a) != 1:
        return f"{name}: ANCHOR-COUNT {rtl.count(a)}"
    src = work / f"{name}.sv"; src.write_text(rtl.replace(a, b))
    mdir = work / f"obj_{name}"
    r = subprocess.run(["make", "-s", "-C", str(root / "tb/verilator/maap"), "build",
                        f"MAAP_RTL={src}", f"MDIR={mdir}", "VERILATOR_JOBS=2",
                        f"VERILATOR={os.environ['VERILATOR']}"], capture_output=True, text=True)
    if r.returncode:
        return f"{name}: BUILD-FAILED\n{r.stderr[-800:]}"
    r = subprocess.run([str(mdir / "VKL_maap_sim")], capture_output=True, text=True)
    (work / f"{name}.out").write_text(r.stdout + r.stderr)
    fails = [l.strip() for l in r.stdout.splitlines() if "[FAIL]" in l]
    verdict = "CAUGHT" if r.returncode == 1 and fails else "ESCAPED" if r.returncode == 0 else f"ABNORMAL rc={r.returncode}"
    return f"{name}: {verdict} rc={r.returncode}\n" + "".join(f"    {l}\n" for l in fails[:8])
work.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(jobs) as ex:
    for line in ex.map(run, PROBES):
        print(line, flush=True)
