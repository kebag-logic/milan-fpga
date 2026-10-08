#!/usr/bin/env python3
"""R548-2 disposable probes on KL_maap at the reviewed head.

Usage: python3 -I r548_2_probes.py <clone> <scratch> <verilator> [--jobs N]

Each probe is an exact single-anchor source replacement applied to a scratch
copy of hdl/ieee1722/maap/KL_maap.sv; the clone is never written. Each copy is
built with the clone's tb/verilator/maap harness (MAAP_RTL/MDIR overrides) and
run. "expect" is KILL (the harness must exit 1) or PASS (an equivalent or
benign change the harness must accept). Prints one line per probe and a tally.
"""
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

SEED = "(mac_seed_w == 16'h0) ? 16'hACE1 : mac_seed_w"
PROBES = (
    # (name, expect, anchor, replacement)
    ("control_unchanged", "PASS", SEED, SEED),
    ("equivalent_fix_other_constant", "PASS", SEED,
     "(mac_seed_w == 16'h0) ? 16'h0001 : mac_seed_w"),
    ("guard_compares_wrong_value", "KILL", SEED,
     "(mac_seed_w == 16'hACE1) ? 16'hACE1 : mac_seed_w"),
    ("seed_forced_zero_always", "KILL", SEED, "16'h0"),
    ("probe_draw_constant", "KILL",
     "16'(PROBE_MIN_MS_C)    + {10'd0, lfsr_r[5:0]}",
     "16'(PROBE_MIN_MS_C)    + 16'd0"),
    ("announce_draw_constant", "KILL",
     "16'(ANNOUNCE_MIN_MS_C) + {6'd0, lfsr_r[9:0]}",
     "16'(ANNOUNCE_MIN_MS_C) + 16'd0"),
    ("probe_draw_one_bit", "PASS?",
     "16'(PROBE_MIN_MS_C)    + {10'd0, lfsr_r[5:0]}",
     "16'(PROBE_MIN_MS_C)    + {15'd0, lfsr_r[0]}"),
    ("defend_guard_only_after_first_beat", "KILL",
     "&& (state_r == ANNOUNCE_S) && !tx_busy_r;",
     "&& (state_r == ANNOUNCE_S) && !(tx_busy_r && tx_beat_r != 3'd0);"),
    ("defend_guard_only_while_stalled", "KILL?",
     "&& (state_r == ANNOUNCE_S) && !tx_busy_r;",
     "&& (state_r == ANNOUNCE_S) && !(tx_busy_r && !m_axis_tready);"),
    ("defend_guard_removed", "KILL",
     "&& (state_r == ANNOUNCE_S) && !tx_busy_r;",
     "&& (state_r == ANNOUNCE_S);"),
    ("own_empty_range_conflicts_in_announce_only", "KILL?",
     " && (count_i != 8'd0)",
     " && ((count_i != 8'd0) || (state_r == ANNOUNCE_S))"),
    ("defend_dst_live_not_latched", "KILL",
     "? tx_dst_r\n", "? rx_src_r\n"),
)


def run(clone: Path, scratch: Path, verilator: str, probe) -> str:
    name, expect, anchor, repl = probe
    src = (clone / "hdl/ieee1722/maap/KL_maap.sv").read_text()
    if src.count(anchor) != 1:
        return f"[ANCHOR] {name}: anchor count {src.count(anchor)}"
    work = scratch / name
    work.mkdir(parents=True, exist_ok=True)
    rtl = work / "KL_maap.sv"
    rtl.write_text(src.replace(anchor, repl))
    b = subprocess.run(["make", "-s", "-C", str(clone / "tb/verilator/maap"), "build",
                        f"MAAP_RTL={rtl}", f"MDIR={work / 'obj'}",
                        f"VERILATOR={verilator}", "VERILATOR_JOBS=1"],
                       capture_output=True, text=True, check=False)
    (work / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return f"[BUILD-FAIL] {name}"
    r = subprocess.run([str(work / "obj/VKL_maap_sim")], capture_output=True,
                       text=True, check=False)
    out = r.stdout + r.stderr
    (work / "run.log").write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if "[FAIL]" in ln]
    verdict = "KILLED" if r.returncode == 1 and fails else (
        "PASSED" if r.returncode == 0 and " 0 failures" in out else f"rc={r.returncode}")
    first = fails[0] if fails else ""
    return f"{name}: expect={expect} result={verdict} fails={len(fails)} first={first}"


def main() -> int:
    clone, scratch, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        for line in ex.map(lambda p: run(clone, scratch, verilator, p), PROBES):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
