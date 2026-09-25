#!/usr/bin/env python3
"""Reviewer fault probes for KL_crf_rx (#541 / PR #562 round R322-1).

Usage: probe_mutants.py <extracted-head-root> <work-dir> <verilator> [jobs]

<extracted-head-root> is `git archive <head> hdl tb` unpacked. Each probe gets
its own copy of tb/verilator/crf_rx (hdl and tb/common are symlinked, never
written), a single-anchor RTL edit, and both receiver harnesses (unit =
sim_main.cpp, discontinuity = sim_discontinuity.cpp) rebuilt from scratch.
A probe is DETECTED when either harness exits nonzero with a [FAIL] line.
Compile failures are reported as INVALID, never as a kill.
"""
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RTL_REL = "hdl/ieee1722/crf/KL_crf_rx.sv"

# name, anchor (must occur exactly once), replacement, intent
PROBES = [
    ("clean", None, None, "positive control: unmodified head"),
    ("P1_error_unlocks_and_counts", "if (!w_fmt_ok) begin",
     "if (!w_fmt_ok) begin\n          if (locked_o) begin locked_o <= 1'b0; "
     "cnt_unlocked_o <= cnt_unlocked_o + 32'd1; end",
     "validation error unlocks and scores MEDIA_UNLOCKED"),
    ("P2_error_refreshes_timeout", "wire w_acc_run_w = w_acc && !stop_i;",
     "wire w_acc_run_w = w_hit && !stop_i;",
     "validation error refreshes the 100 ms timeout (doc: does not)"),
    ("P3_error_keeps_settling",
     "          settle_r  <= '0;\n        end else begin\n          //! FRAMES_RX",
     "        end else begin\n          //! FRAMES_RX",
     "validation error no longer breaks settling (doc: breaks settling)"),
    ("P4_error_counts_frames_rx", "if (iv_frx_r || w_acc)",
     "if (iv_frx_r || w_acc || w_ev_uf_w)",
     "validation error also commits FRAMES_RX"),
    ("P4b_error_flags_frames_rx", "iv_frx_r <= iv_frx_r | w_acc;",
     "iv_frx_r <= iv_frx_r | w_hit;",
     "validation error raises the FRAMES_RX interval flag (P4 only hit the tick cycle)"),
    ("P5_error_unlocks_at_commit", "        if (iv_uf_r || w_ev_uf_w)\n          fmt_err_o <= fmt_err_o + 32'd1;",
     "        if (iv_uf_r || w_ev_uf_w) begin\n          fmt_err_o <= fmt_err_o + 32'd1;\n"
     "          locked_o <= 1'b0;\n        end",
     "lock dropped at the UNSUPPORTED_FORMAT interval commit"),
    ("P6_timeout_long", "localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10;",
     "localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10 + 50;",
     "timeout 50 cycles (250 us at 200 kHz) late"),
    ("P7_timeout_short", "localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10;",
     "localparam int unsigned TOUT_CYC_C = CLK_FREQ_HZ_P / 10 - 50;",
     "timeout 50 cycles early"),
    ("P8_error_counts_per_pdu", "        if (iv_uf_r || w_ev_uf_w)\n          fmt_err_o <= fmt_err_o + 32'd1;",
     "        if (1'b0)\n          fmt_err_o <= fmt_err_o + 32'd1;",
     "UNSUPPORTED_FORMAT interval commit removed (never counts)"),
    ("P9_error_unlock_delayed", "  always_ff @(posedge clk_i) begin : engine",
     "  logic uf_d1_r, uf_d2_r;\n  always_ff @(posedge clk_i) begin\n"
     "    uf_d1_r <= w_ev_uf_w; uf_d2_r <= uf_d1_r;\n  end\n"
     "  always_ff @(posedge clk_i) begin : engine",
     "helper for P9 (paired edit below)"),
]
# P9 needs a second edit: drop lock two cycles after a reject.
P9_SECOND = ("      if (w_bind_rise_w) begin\n        hfill_r <= '0;",
             "      if (uf_d2_r) locked_o <= 1'b0;\n"
             "      if (w_bind_rise_w) begin\n        hfill_r <= '0;")


def run(cmd, cwd, log):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    log.write(f"$ {' '.join(map(str, cmd))}\nrc={r.returncode}\n{r.stdout[-6000:]}{r.stderr[-3000:]}\n")
    return r


def probe(root: Path, work: Path, verilator: str, spec):
    name, anchor, repl, intent = spec
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    (d / "tb/verilator").mkdir(parents=True)
    os.symlink(root / "hdl", d / "hdl")
    os.symlink(root / "tb/common", d / "tb/common")
    shutil.copytree(root / "tb/verilator/crf_rx", d / "tb/verilator/crf_rx")
    # Cap the builder's own parallelism (the suite asks for -j 0 = all cores).
    mk = d / "tb/verilator/crf_rx/Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 8"))
    src = (root / RTL_REL).read_text()
    if anchor is not None:
        if src.count(anchor) != 1:
            return {"name": name, "intent": intent, "verdict": "INVALID", "why": "anchor count"}
        src = src.replace(anchor, repl)
        if name == "P9_error_unlock_delayed":
            if src.count(P9_SECOND[0]) != 1:
                return {"name": name, "intent": intent, "verdict": "INVALID", "why": "anchor2"}
            src = src.replace(P9_SECOND[0], P9_SECOND[1])
    rtl = d / "mut.sv"
    rtl.write_text(src)
    tbd = d / "tb/verilator/crf_rx"
    out = {"name": name, "intent": intent}
    with open(d / "probe.log", "w") as log:
        for leg, target, exe in (("unit", "unit", None), ("disc", "discontinuity", None)):
            r = run(["make", "-s", target, f"VERILATOR={verilator}", f"RX_RTL={rtl}"], tbd, log)
            text = r.stdout + r.stderr
            if "%Error" in text and "[FAIL]" not in text and "[PASS]" not in text:
                out[leg] = {"rc": r.returncode, "state": "BUILD_ERROR"}
                continue
            fails = [l.strip() for l in text.splitlines() if "[FAIL]" in l]
            summary = [l.strip() for l in text.splitlines()
                       if ("checks" in l and "failures" in l)]
            out[leg] = {"rc": r.returncode, "fail_lines": fails[:12],
                        "n_fail_lines": len(fails), "summary": summary}
    legs = [out.get("unit", {}), out.get("disc", {})]
    if any(l.get("state") == "BUILD_ERROR" for l in legs):
        out["verdict"] = "INVALID"
    elif anchor is None:
        out["verdict"] = "CONTROL_PASS" if all(l["rc"] == 0 and not l["n_fail_lines"] for l in legs) else "CONTROL_FAIL"
    else:
        out["verdict"] = "DETECTED" if any(l["rc"] != 0 and l["n_fail_lines"] for l in legs) else "SURVIVED"
    return out


def main():
    root, work, verilator = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    only = os.environ.get("PROBES")
    specs = [p for p in PROBES if not only or p[0] in only.split(",")]
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=min(jobs, 8)) as ex:
        results = list(ex.map(lambda s: probe(root, work, verilator, s), specs))
    for r in results:
        print(f"{r['name']:32s} {r['verdict']:13s} {r['intent']}")
        for leg in ("unit", "disc"):
            if leg in r:
                l = r[leg]
                print(f"    {leg}: rc={l.get('rc')} {l.get('state','')} fails={l.get('n_fail_lines')} "
                      f"{' | '.join(l.get('summary', []))}")
                for f in l.get("fail_lines", [])[:4]:
                    print(f"      {f}")
    print(json.dumps(results, indent=1), file=open(work / "probe-results.json", "w"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
