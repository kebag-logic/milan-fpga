#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe campaign for #546 / PR #554 (round R302-1).

Usage: VERILATOR=<verilator 5.050> python3 run_probes.py <clone> <packet>

Extracts the exact reviewed commit's hdl/ and tb/ with `git archive` into
<packet>/scratch/probe-tree (the clone is never edited), then builds:
  * the shipped discontinuity and talker_step harnesses, and the servo unit
    harness, against clean and mutated RTL copies;
  * the reviewer probes probe_jitter.cpp and probe_loop.cpp.
Every mutant declares whether a named harness must FAIL. A compile error
never counts as a kill. At most 8 builds run at once.
"""

import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HEAD = "39a0171c8c39e68065b14b9178b30d708a9f7645"
VER = os.environ.get("VERILATOR", "verilator")
RX = "hdl/ieee1722/crf/KL_crf_rx.sv"
SERVO = "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv"

RX_FLAGS = ["-GCLK_FREQ_HZ_P=200000", "-GIVAL_CYC_P=200",
            "-GMAXTT_NS_P=2000000", "-GEARLY_MARGIN_NS_P=10000000"]
WARN = ["-Wall", "-Wno-fatal", "-Wno-DECLFILENAME", "-Wno-UNUSEDSIGNAL",
        "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC", "-Wno-UNUSEDPARAM",
        "-Wno-EOFNEWLINE", "-Wno-PINCONNECTEMPTY"]
UNIT_G = ["-GTICK_CYC_P=3072", "-GWIN_LOG2_P=5", "-GNOM_WIN_NS_P=64'd4000000",
          "-GNORM_SHIFT_P=7", "-GGAIN_NUM_P=7", "-GRELOCK_TOUT_P=20000",
          "-GLOCK_THR_P=8192"]

# (name, file, anchor, replacement, {harness: expected verdict})
# expected: "FAIL" = must fail (kill), "PASS" = must pass, "INFO" = record only
MUTANTS = [
    ("servo_ignores_valid", SERVO,
     "\n                           && crf_rate_valid_i;", ";",
     {"talker": "INFO", "unit": "FAIL", "loop:talker_only_neg": "INFO"}),
    ("rx_no_detection", RX,
     "wire rate_break_w = w_acc && rate_seeded_r &&",
     "wire rate_break_w = 1'b0 && w_acc && rate_seeded_r &&",
     {"talker": "INFO", "disc": "FAIL", "loop:talker_only_neg": "FAIL",
      "loop:talker_only_pos": "FAIL", "loop:lag_sweep": "FAIL"}),
    ("jump_removed", RX, "tu_change_w || ts_jump_w ||", "tu_change_w || 1'b0 ||",
     {"talker": "INFO", "disc": "FAIL", "loop:talker_only_neg": "FAIL"}),
    ("tu_ignored", RX, "wire tu_change_w = tu_i != prev_tu_r;",
     "wire tu_change_w = 1'b0;",
     {"talker": "INFO", "disc": "FAIL", "loop:tu_only": "FAIL",
      "loop:talker_only_pos": "INFO"}),
    ("seq_gap_removed", RX, "|| (have_seq_r && (seq_i != exp_seq_r)));",
     "|| 1'b0);", {"disc": "FAIL"}),
    ("silence_keeps_valid", RX,
     "          rate_seeded_r <= 1'b0;\n          rate_valid_r <= 1'b0;\n",
     "          rate_seeded_r <= 1'b0;\n", {"disc": "FAIL"}),
    ("bind_keeps_valid", RX,
     "        rate_seeded_r <= 1'b0;\n        rate_valid_r <= 1'b0;\n        mr_seeded_r",
     "        rate_seeded_r <= 1'b0;\n        mr_seeded_r", {"disc": "FAIL"}),
    ("stop_ungated", RX, "rate_valid_r && en_i && !stop_i &&",
     "rate_valid_r && en_i &&", {"disc": "FAIL"}),
    ("refill_long", RX, "hfill_r <= 9'd1;", "hfill_r <= 9'd0;", {"disc": "FAIL"}),
    ("break_keeps_valid", RX,
     "hfill_r <= 9'd1;\n            rate_valid_r <= 1'b0;", "hfill_r <= 9'd1;",
     {"disc": "FAIL"}),
    ("pending_not_cancelled", RX, "if (rate_pend_r && !rate_break_w) begin",
     "if (rate_pend_r) begin", {"disc": "FAIL"}),
    ("thr_doubled", RX, "64'd1 << $clog2(RATE_DRIFT_NS_C + 2 * 384);",
     "64'd1 << ($clog2(RATE_DRIFT_NS_C + 2 * 384) + 1);", {"disc": "FAIL"}),
    ("thr_halved", RX, "64'd1 << $clog2(RATE_DRIFT_NS_C + 2 * 384);",
     "64'd1 << ($clog2(RATE_DRIFT_NS_C + 2 * 384) - 1);",
     {"disc": "FAIL", "jitter": "FAIL"}),
    ("spacing_32bit", RX, "wire [63:0] ts_spacing_ns_w = w_crf_ts - prev_ts_ns_r;",
     "wire [63:0] ts_spacing_ns_w = 64'(w_crf_ts[31:0] - prev_ts_ns_r[31:0]);",
     {"disc": "FAIL"}),
    ("lower_bound_removed", RX,
     "(ts_spacing_ns_w < (64'(NOM_PDU_NS_C) - TS_JUMP_NS_C))",
     "1'b0", {"disc": "FAIL", "talker": "INFO", "loop:talker_only_neg": "FAIL"}),
]
LOOP_SCENARIOS = ["tu_only", "step_inside_tu", "step20us", "local_first",
                  "repeated", "quiet", "talker_only_neg", "talker_only_pos",
                  "lag_sweep"]
INFO_SCENARIOS = ["subthreshold"]


def sh(cmd, cwd, log):
    with open(log, "a") as f:
        f.write("$ " + " ".join(cmd) + "\n")
        f.flush()
        r = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
    return r.returncode


def build(tree, rtl_rx, rtl_servo, harness, mdir, log):
    tb = tree / "tb/verilator/crf_rx"
    common = [str(tree / "hdl/common/cdc_pulse.sv"),
              str(tree / "hdl/common/cdc_handshake.sv")]
    base = [VER, "--cc", "--exe", "--build", "-j", "1", "--public-flat-rw",
            "-Mdir", str(mdir)] + WARN + ["-CFLAGS", "-std=c++17 -O2"]
    if harness in ("disc", "jitter"):
        src = "sim_discontinuity.cpp" if harness == "disc" else str(
            tree / "tb/verilator/crf_rx_probe/probe_jitter.cpp")
        cmd = base + ["--top-module", "KL_crf_rx"] + RX_FLAGS + \
            [str(rtl_rx), src, "-o", "Vh"]
    elif harness in ("talker", "loop"):
        src = "sim_talker_step.cpp" if harness == "talker" else str(
            tree / "tb/verilator/crf_rx_probe/probe_loop.cpp")
        cmd = base + ["--top-module", "crf_talker_wrap", str(rtl_rx)] + common + \
            [str(rtl_servo), "crf_talker_wrap.sv", src, "-o", "Vh"]
    elif harness == "unit":
        tb = tree / "tb/verilator/mmcm_servo"
        cmd = base + ["--top-module", "KL_mmcm_drp_servo"] + UNIT_G + common + \
            [str(rtl_servo), "sim_main.cpp", "-o", "Vh"]
    else:
        raise ValueError(harness)
    return sh(cmd, tb, log)


def verdict(log_text, rc):
    if rc == 0 and ("failures: 0 " in log_text or " 0 failures" in log_text):
        return "PASS"
    if rc == 1 and ("RESULT: FAIL" in log_text or " 0 failures" not in log_text):
        return "FAIL"
    return f"ABNORMAL(rc={rc})"


def build_job(tree, name, rtl_rx, rtl_servo, kind, out):
    mdir = tree.parent / "obj" / f"{name}__{kind}"
    mdir.mkdir(parents=True, exist_ok=True)
    log = out / f"{name}__{kind}.build.log"
    log.unlink(missing_ok=True)
    return (name, kind), build(tree, rtl_rx, rtl_servo, kind, mdir, log)


def run_job(tree, out, name, harness, expect, built):
    kind, _, scen = harness.partition(":")
    if built[(name, kind)]:
        return name, harness, expect, "COMPILE_ERROR"
    mdir = tree.parent / "obj" / f"{name}__{kind}"
    log = out / f"{name}__{harness.replace(':', '_')}.log"
    r = subprocess.run([str(mdir / "Vh")] + ([scen] if scen else []),
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, timeout=3600)
    log.write_text(r.stdout + f"\nexit status {r.returncode}\n")
    return name, harness, expect, verdict(r.stdout, r.returncode)


def main():
    clone, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    head = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != HEAD:
        print(f"refusing: clone HEAD {head} is not {HEAD}")
        return 2
    root = packet / "scratch" / "probe-run"
    shutil.rmtree(root, ignore_errors=True)
    tree = root / "tree"
    tree.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", str(clone), "archive", HEAD, "hdl", "tb"],
                          capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=arch, check=True)
    probe_dir = tree / "tb/verilator/crf_rx_probe"
    probe_dir.mkdir()
    for f in ("probe_jitter.cpp", "probe_loop.cpp"):
        shutil.copy(packet / "probes" / f, probe_dir / f)
    out = packet / "receipts" / "probes"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    mut = root / "mut"
    mut.mkdir()

    clean_rx, clean_servo = tree / RX, tree / SERVO
    jobs = [("clean", clean_rx, clean_servo, h, "PASS")
            for h in ("disc", "talker", "unit", "jitter")]
    jobs += [("clean", clean_rx, clean_servo, f"loop:{s}", "PASS")
             for s in LOOP_SCENARIOS]
    jobs += [("clean", clean_rx, clean_servo, f"loop:{s}", "INFO")
             for s in INFO_SCENARIOS]
    for name, path, anchor, repl, expects in MUTANTS:
        src = (tree / path).read_text()
        if src.count(anchor) != 1:
            print(f"ANCHOR {name}: expected exactly one, found {src.count(anchor)}")
            return 1
        d = mut / name
        d.mkdir()
        mutated = d / Path(path).name
        mutated.write_text(src.replace(anchor, repl, 1))
        rx = mutated if path == RX else clean_rx
        servo = mutated if path == SERVO else clean_servo
        jobs += [(name, rx, servo, h, e) for h, e in expects.items()]

    ok = True
    builds = {}
    for name, rx, servo, harness, _ in jobs:
        builds.setdefault((name, harness.partition(":")[0]), (name, rx, servo))
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(build_job, tree, n, rx, sv, k, out)
                for (n, k), (_, rx, sv) in builds.items()]
        built = dict(f.result() for f in futs)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(run_job, tree, out, n, h, e, built)
                for n, _, _, h, e in jobs]
        rows = [f.result() for f in futs]
    with open(out / "SUMMARY.txt", "w") as s:
        s.write(f"head {HEAD}\nverilator {subprocess.run([VER, '--version'], capture_output=True, text=True).stdout.strip()}\n")
        for name, harness, expect, got in rows:
            good = expect == "INFO" or got == expect
            ok &= good
            line = f"{'OK ' if good else 'BAD'} {name:24s} {harness:22s} expect={expect:5s} got={got}"
            print(line)
            s.write(line + "\n")
        s.write(f"campaign {'PASS' if ok else 'FAIL'}\n")
    print("campaign", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
