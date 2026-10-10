#!/usr/bin/env python3
# [R558] R558-7 reviewer planted-defect probes on KL_maap.sv (unit harness).
# Each probe is an exact single-anchor replacement applied to a scratch copy;
# no checkout file is edited. A probe is CAUGHT when the build succeeds, the
# harness exits 1 and at least one [FAIL] line is printed; ESCAPED when the
# harness exits 0 with " 0 failures"; anything else is reported as ERROR.
# usage: reviewer_probes.py <clone> <workdir> [--jobs N] [names...]
import argparse, concurrent.futures as cf, os, subprocess, sys
from pathlib import Path

PROBES = {
    # M2 (B.3.6.6): echo the overlap start instead of the PROBE's requested start
    "q1_m2_echo_overlap_start": ("tx_defend_off_r <= rx_start_r;", "tx_defend_off_r <= conf_start_w;"),
    # M4: first offset folds the unstepped seed (the ruling asks for one generator step)
    "q2_first_offset_unstepped": ("offset_fold(seed_next_w), count_i)", "offset_fold(enable_seed_w), count_i)"),
    # M4: probe draw folds the unstepped state (disclosed by the author as ungraded)
    "q3_probe_fold_unstepped": ("{10'd0, probe_fold(lfsr_next_w)}", "{10'd0, probe_fold(lfsr_r)}"),
    # informational: every Begin! re-folds MAC+clock instead of reading the running generator
    "q4_every_begin_refolds": ("rand_offset(rng_seeded_r ? lfsr_next_w[15:0]", "rand_offset(1'b0 ? lfsr_next_w[15:0]"),
    # M8: missing-byte state does not accumulate across beats
    "q6_m8_no_accumulate": ("rx_bytes_valid_r <= rx_beat_complete_w && ((rbeat_r == '0) || rx_bytes_valid_r);",
                            "rx_bytes_valid_r <= rx_beat_complete_w;"),
    # M5: link return counts as a conflict
    "q7_m5_counts_conflict": ("            if (restart_w)\n              conflicts_o",
                              "            if (1'b1)\n              conflicts_o"),
    # M1: equal MAC treated as lower
    "q11_m1_equal_is_lower": ("octet_rev(station_mac_i) < octet_rev(rx_src_r)",
                              "octet_rev(station_mac_i) <= octet_rev(rx_src_r)"),
    # M7: supplied seed end compared one short (count off by one)
    "q12_m7_end_off_by_one": ("seed_end_w <= {1'b0, POOL_SIZE_C}", "seed_end_w <= {1'b0, POOL_SIZE_C} + 17'd1"),
    # M6: a pending DEFEND survives a conflict restart only (not disable/link)
    "q13_m6_survives_restart": ("if (!enable_i || restart_w || port_operational_p)",
                                "if (!enable_i || port_operational_p)"),
    # M5: link return ignored while PROBE only
    "q14_m5_return_only_in_announce": ("else if (restart_w || port_operational_p)",
                                       "else if (restart_w || (port_operational_p && state_r == ANNOUNCE_S))"),
}


def run(clone: Path, work: Path, name: str) -> str:
    anchor, repl = PROBES[name]
    src = (clone / "hdl/ieee1722/maap/KL_maap.sv").read_text()
    if src.count(anchor) != 1:
        return f"[ERROR] {name}: anchor count {src.count(anchor)}"
    rtl = work / f"{name}.sv"
    rtl.write_text(src.replace(anchor, repl))
    mdir = work / f"obj_{name}"
    b = subprocess.run(["make", "-s", "-C", str(clone / "tb/verilator/maap"), "build",
                        f"MAAP_RTL={rtl}", f"MDIR={mdir}",
                        f"VERILATOR={os.environ['VERILATOR']}", "VERILATOR_JOBS=2"],
                       capture_output=True, text=True)
    log = work / f"{name}.log"
    if b.returncode:
        log.write_text(b.stdout + b.stderr)
        return f"[ERROR] {name}: build rc={b.returncode}"
    r = subprocess.run([str(mdir / "VKL_maap_sim")], cwd=mdir, capture_output=True, text=True)
    out = r.stdout + r.stderr
    log.write_text(out)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    if r.returncode == 1 and fails:
        return f"[CAUGHT] {name}: rc=1, {len(fails)} failing checks; first: {fails[0]}"
    if r.returncode == 0 and " 0 failures" in out:
        return f"[ESCAPED] {name}: rc=0, {out.strip().splitlines()[-1] if out.strip() else ''}"
    return f"[ERROR] {name}: rc={r.returncode}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("clone", type=Path); ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=4); ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    names = a.names or list(PROBES)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for line in ex.map(lambda n: run(a.clone, a.work, n), names):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
