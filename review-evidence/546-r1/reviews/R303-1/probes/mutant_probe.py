#!/usr/bin/env python3
"""Reviewer mutation/probe runner for PR #554 (issue #546).

Usage: mutant_probe.py <exported-head-tree> <work-dir> <verilator> [case ...]

Each case copies hdl/ and tb/ of the exported exact-head tree into its own
work directory, applies one textual mutation (exactly one anchor match is
required), and runs one target:
  disc   -> make -C tb/verilator/crf_rx discontinuity   (C++ build -j 4)
  talker -> make -C tb/verilator/crf_rx talker_step      (-j 4 in Makefile)
  probe  -> reviewer probe_talker.cpp against crf_talker_wrap
  order  -> reviewer probe_gm_order.cpp (listener-first GM change), same wrap
A mutant counts as KILLED only on nonzero rc with RESULT: FAIL printed by
the harness (make wraps the harness's rc 1 as 2); a build error is never a kill. At most two cases run at once (2 x -j 4 = 8 jobs).
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
SV = "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"
CASES = [
    # name, target, file, anchor, replacement, expected (clean|kill)
    ("clean_disc", "disc", None, None, None, "clean"),
    ("clean_talker", "talker", None, None, None, "clean"),
    ("clean_probe", "probe", None, None, None, "clean"),
    ("C1_tu_ignored", "talker", RX, "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = 1'b0;", "report"),
    ("C2_jump_removed", "talker", RX, "tu_change_w || ts_jump_w ||",
     "tu_change_w || 1'b0 ||", "kill"),
    ("C3_tu_and_jump_removed", "talker", RX, "tu_change_w || ts_jump_w ||",
     "1'b0 || 1'b0 ||", "kill"),
    ("C4_servo_ignores_valid", "talker", SV,
     "(state_r != HOLDOVER_S)\n                           && crf_rate_valid_i;",
     "(state_r != HOLDOVER_S);", "kill"),
    ("C5_rx_valid_forced", "talker", RX,
     "assign rate_valid_o = rate_valid_r && en_i && !stop_i &&",
     "assign rate_valid_o = 1'b1 || en_i && !stop_i &&", "kill"),
    ("D1_seq_gap_ignored", "disc", RX,
     "(tu_change_w || ts_jump_w || (have_seq_r && (seq_i != exp_seq_r)));",
     "(tu_change_w || ts_jump_w);", "kill"),
    ("D2_stop_gate_removed", "disc", RX,
     "assign rate_valid_o = rate_valid_r && en_i && !stop_i &&",
     "assign rate_valid_o = rate_valid_r && en_i &&", "kill"),
    ("D3_silence_keeps_valid", "disc", RX,
     "          rate_valid_r <= 1'b0;\n          rate_pend_r <= 1'b0;\n          mr_seeded_r",
     "          rate_pend_r <= 1'b0;\n          mr_seeded_r", "kill"),
    ("D4_bind_keeps_valid", "disc", RX,
     "        rate_valid_r <= 1'b0;\n        mr_seeded_r <= 1'b0;\n        have_seq_r  <= 1'b0;",
     "        mr_seeded_r <= 1'b0;\n        have_seq_r  <= 1'b0;", "kill"),
    ("D5_spacing_32bit", "disc", RX,
     "wire [63:0] ts_spacing_ns_w = w_crf_ts - prev_ts_ns_r;",
     "wire [63:0] ts_spacing_ns_w = {32'd0, w_crf_ts[31:0] - prev_ts_ns_r[31:0]};",
     "kill"),
    ("D6_pend_not_cancelled", "disc", RX,
     "if (rate_pend_r && !rate_break_w) begin", "if (rate_pend_r) begin", "kill"),
    ("D7_threshold_4096", "disc", RX,
     "64'd1 << $clog2(RATE_DRIFT_NS_C + 2 * 384);", "64'd4096;", "kill"),
    ("D8_threshold_1024", "disc", RX,
     "64'd1 << $clog2(RATE_DRIFT_NS_C + 2 * 384);", "64'd1024;", "kill"),
    ("D9_break_keeps_valid", "disc", RX,
     "hfill_r <= 9'd1;\n            rate_valid_r <= 1'b0;", "hfill_r <= 9'd1;", "kill"),
    ("D10_tu_rise_only", "disc", RX, "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = tu_i && !prev_tu_r;", "kill"),
    # listener-first GM change (probe_gm_order.cpp): discriminating variant
    ("O0_clean", "order", None, None, None, "clean"),
    ("O1_tu_ignored", "order", RX, "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = 1'b0;", "report"),
    ("O2_jump_removed", "order", RX, "tu_change_w || ts_jump_w ||",
     "tu_change_w || 1'b0 ||", "kill"),
    ("O3_tu_and_jump_removed", "order", RX, "tu_change_w || ts_jump_w ||",
     "1'b0 || 1'b0 ||", "kill"),
    ("O4_servo_ignores_valid", "order", SV,
     "(state_r != HOLDOVER_S)\n                           && crf_rate_valid_i;",
     "(state_r != HOLDOVER_S);", "kill"),
]


def run(src: Path, work: Path, verilator: str, case) -> str:
    name, target, rel, anchor, repl, expect = case
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    for part in ("hdl", "tb"):
        shutil.copytree(src / part, root / part, symlinks=True,
                        ignore=shutil.ignore_patterns("obj_*"))
    if rel:
        path = root / rel
        text = path.read_text()
        if text.count(anchor) != 1:
            return f"{name}: ANCHOR-COUNT {text.count(anchor)} (not run)"
        path.write_text(text.replace(anchor, repl))
    tbdir = root / "tb/verilator/crf_rx"
    mk = tbdir / "Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 4"))
    if target == "disc":
        cmd = ["make", "-s", "-C", str(tbdir), "discontinuity", f"VERILATOR={verilator}"]
    elif target == "talker":
        cmd = ["make", "-s", "-C", str(tbdir), "talker_step", f"VERILATOR={verilator}"]
    else:
        cpp = "probe_talker.cpp" if target == "probe" else "probe_gm_order.cpp"
        shutil.copy(Path(__file__).with_name(cpp), tbdir / "probe_talker.cpp")
        hdl = root / "hdl"
        cmd = ["sh", "-c",
               f"cd {tbdir} && {verilator} --cc --exe --build -j 4 --public-flat-rw "
               "--top-module crf_talker_wrap -Mdir obj_probe -Wall -Wno-fatal "
               "-Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -Wno-PINCONNECTEMPTY "
               "-CFLAGS '-std=c++17 -O2' "
               f"{hdl}/ieee1722/crf/KL_crf_rx.sv {hdl}/common/cdc_pulse.sv "
               f"{hdl}/common/cdc_handshake.sv {hdl}/ieee1722/crf/KL_mmcm_drp_servo.sv "
               "crf_talker_wrap.sv probe_talker.cpp -o Vprobe >/dev/null && ./obj_probe/Vprobe"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    out = res.stdout + res.stderr
    (work / f"{name}.log").write_text(out)
    built = "RESULT:" in out or "checks" in out
    failed = res.returncode != 0 and "RESULT: FAIL" in out  # make: rc 2
    if not built:
        verdict = "BUILD-OR-RUN-ERROR"
    elif expect == "clean":
        verdict = "PASS" if res.returncode == 0 else "UNEXPECTED-FAIL"
    elif expect == "kill":
        verdict = "KILLED" if failed else "SURVIVED"
    else:
        verdict = "FAILS" if failed else "PASSES"
    fails = sorted({l.strip() for l in out.splitlines() if "[FAIL]" in l})
    lines = [f"{name}: target={target} expect={expect} rc={res.returncode} -> {verdict}"]
    lines += [f"    {l}" for l in fails[:8]]
    lines += [f"    {l}" for l in out.splitlines()
              if l.startswith(("[probe]", "step ", "steady", "== "))]
    return "\n".join(lines)


def main() -> int:
    src, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    verilator = sys.argv[3]
    work.mkdir(parents=True, exist_ok=True)
    cases = [c for c in CASES if len(sys.argv) < 5 or c[0] in sys.argv[4:]]
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda c: run(src, work, verilator, c), cases))
    print("\n".join(results))
    bad = [r for r in results if " -> " in r and r.split(" -> ")[1].split("\n")[0]
           in ("SURVIVED", "UNEXPECTED-FAIL", "BUILD-OR-RUN-ERROR")]
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
