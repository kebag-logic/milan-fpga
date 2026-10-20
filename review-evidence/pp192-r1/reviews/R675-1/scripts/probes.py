#!/usr/bin/env python3
"""Reviewer-planted probes for processor issue #192 at an extracted head.

Each probe copies hdl/, tb/common/ and the bench it needs from the extracted
tree into a disposable directory, plants one exact edit (count-checked), builds
with the given Verilator and runs one bench mode. A mutant is KILLED when the
run fails (rc != 0) with at least one FAIL line starting with its expected
check. The oracle probe adds a simulation-only monitor to the listener and
must PASS while reporting zero mismatches.

usage: probes.py --tree T --output O --verilator V [--jobs N] [--only NAME...]
"""
import argparse
import concurrent.futures as cf
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

LSTN = "hdl/acmp/KL_pp_acmp_listener.sv"
TOP = "hdl/top/protocol_processor_top.sv"
NTFY = "hdl/aecp/KL_aecp_notify.sv"

# A started/stopped oracle: any record write (walk write-back, preload or
# sweep) that keeps the sink bound and flips f_started must be followed, on
# the next clock, by exactly one act_strt_chg_o pulse, and no pulse may come
# without one. Independent of the walk's own strt_was_r/bnd_was_r.
ORACLE = """  assign dbg_busy_o       = (xs_r != X_IDLE);
  // ---- reviewer oracle (disposable probe, never committed) ----
  logic [N_SINKS_P-1:0] or_bnd_q, or_strt_q;
  logic or_exp_r;
  int unsigned or_chg_n, or_bad_n, or_nonwb_n;
  initial begin or_chg_n = 0; or_bad_n = 0; or_nonwb_n = 0; end
  always_ff @(posedge clk_i) begin : reviewer_oracle
    if (!rst_n) begin
      or_bnd_q  <= '0;
      or_strt_q <= '0;
      or_exp_r  <= 1'b0;
    end else begin
      or_exp_r <= 1'b0;
      if (recwr_en_w) begin
        or_bnd_q[recwr_addr_w]  <= recwr_rec_w.f_bound;
        or_strt_q[recwr_addr_w] <= recwr_rec_w.f_started;
        if (or_bnd_q[recwr_addr_w] && recwr_rec_w.f_bound
            && (or_strt_q[recwr_addr_w] != recwr_rec_w.f_started)) begin
          or_exp_r <= 1'b1;
          or_chg_n <= or_chg_n + 1;
          if (xs_r != X_WB) or_nonwb_n <= or_nonwb_n + 1;
        end
      end
      if (or_exp_r != act_strt_chg_o) begin
        or_bad_n <= or_bad_n + 1;
        $display("R675-ORACLE MISMATCH t=%0t expected=%0d pulse=%0d sink=%0d",
                 $time, or_exp_r, act_strt_chg_o, sink_r);
      end
    end
  end
  final $display("R675-ORACLE bound started/stopped changes=%0d not-by-walk=%0d mismatches=%0d",
                 or_chg_n, or_nonwb_n, or_bad_n);
"""

PROBES = [
    # name, bench, mode args, [(file, old, new, count)], expected FAIL prefix
    ("gsi-round-excludes-requester", "pp_top", ["--gsi-internal-only"],
     [(NTFY,
       "                end else begin\n"
       "                  em_excl_v_r <= 1'b0;\n"
       "                  if (pick_kind_w == PP_UNS_AVB_C)",
       "                end else begin\n"
       "                  em_excl_r   <= ev_cmd_excl_eid_i;\n"
       "                  em_excl_v_r <= (pick_dt_w == 16'h0005);\n"
       "                  if (pick_kind_w == PP_UNS_AVB_C)", 1)],
     "GI STOP-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester"),
    ("started-only-on-stop", "pp_top", ["--gsi-internal-only"],
     [(LSTN, "&& (rec_r.f_started != strt_was_r);",
       "&& strt_was_r && !rec_r.f_started;", 1)],
     "GI START-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester"),
    ("started-pulse-repeated", "pp_top", ["--gsi-internal-only"],
     [(TOP,
       "  always_comb begin : stri_events\n",
       "  logic [9:0] rv_dly_r;\n"
       "  logic [SINK_IDX_W_C-1:0] rv_sink_r;\n"
       "  always_ff @(posedge clk_i) begin : reviewer_repeat\n"
       "    if (!rst_n) rv_dly_r <= '0;\n"
       "    else if (lstn_act_strt_chg_w) begin\n"
       "      rv_dly_r <= 10'd600; rv_sink_r <= lstn_act_sink_w;\n"
       "    end else if (rv_dly_r != 0) rv_dly_r <= rv_dly_r - 10'd1;\n"
       "  end\n"
       "  always_comb begin : stri_events\n", 1),
      (TOP,
       "          (32'(lstn_act_sink_w) == k && lstn_act_strt_chg_w)\n",
       "          (32'(lstn_act_sink_w) == k && lstn_act_strt_chg_w)\n"
       "          || (32'(rv_sink_r) == k && rv_dly_r == 10'd1)\n", 1)],
     "GI STOP-BY-A: exactly one GET_STREAM_INFO for sink 0 at A, the requester"),
    ("started-term-sink-0", "pp_top", ["--arm-queue-only"],
     [(TOP, "(32'(lstn_act_sink_w) == k && lstn_act_strt_chg_w)",
       "(k == 0 && lstn_act_strt_chg_w)", 1)],
     "G7f: the STOP requester receives the u=1 GET_STREAM_INFO for sink 1"),
    ("oracle-pp_top-default", "pp_top", [],
     [(LSTN, "  assign dbg_busy_o       = (xs_r != X_IDLE);\n", ORACLE, 1)], None),
    ("oracle-acmp_listener", "acmp_listener", None,
     [(LSTN, "  assign dbg_busy_o       = (xs_r != X_IDLE);\n", ORACLE, 1)], None),
    ("oracle-acmp_nvm", "acmp_nvm", None,
     [(LSTN, "  assign dbg_busy_o       = (xs_r != X_IDLE);\n", ORACLE, 1)], None),
    # oracle sensitivity: the defect as reported must show as mismatches
    ("oracle-sensitivity-acmp_nvm", "acmp_nvm", None,
     [(LSTN, "  assign dbg_busy_o       = (xs_r != X_IDLE);\n", ORACLE, 1),
      (LSTN, "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n",
       "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound && !src_strq_r\n", 1)],
     "ORACLE-MISMATCH"),
]


def sh(cmd, cwd, log, env):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                              env=env, check=False).returncode


def probe(spec, tree, out, verilator, scratch):
    name, bench, mode, edits, expected = spec
    t0 = time.time()
    env = dict(os.environ)
    env["PATH"] = str(Path(verilator).parent) + os.pathsep + env["PATH"]
    with tempfile.TemporaryDirectory(prefix=f"r675-{name}-", dir=scratch) as tmp:
        root = Path(tmp)
        for d in ("hdl", "tb/common", f"tb/{bench}", "scripts"):
            shutil.copytree(tree / d, root / d, symlinks=True,
                            ignore=shutil.ignore_patterns("obj*", "__pycache__"))
        for fname, old, new, count in edits:
            p = root / fname
            s = p.read_text()
            if s.count(old) != count:
                raise RuntimeError(f"{name}: {fname}: {s.count(old)} sites, want {count}")
            p.write_text(s.replace(old, new))
        b = root / "tb" / bench
        if mode is None:   # the bench's own default target
            build_rc = 0
            run_rc = sh(["make", "VERILATOR=" + verilator], b, out / f"{name}-run.log", env)
        else:
            build_rc = sh(["make", "gsi-build", "VERILATOR=" + verilator], b,
                          out / f"{name}-build.log", env)
            if build_rc != 0:
                raise RuntimeError(f"{name}: build failed rc={build_rc}")
            run_rc = sh(["./obj_dir/Vpp_top_sim", *mode], b, out / f"{name}-run.log", env)
    text = (out / f"{name}-run.log").read_text(errors="replace")
    fails = [l for l in text.splitlines() if l.startswith("FAIL")]
    if expected == "ORACLE-MISMATCH":
        mism = [l for l in text.splitlines() if l.startswith("R675-ORACLE MISMATCH")]
        verdict = "KILLED" if mism else "SURVIVED"
        detail = {"expected": expected, "mismatch_lines": len(mism), "first": mism[:3]}
    elif expected is None:
        oracle = [l for l in text.splitlines() if l.startswith("R675-ORACLE")]
        mism = [l for l in oracle if "MISMATCH" in l]
        finals = [l for l in oracle if "changes=" in l]
        ok = (run_rc == 0 and not fails and not mism and finals
              and all("mismatches=0" in l for l in finals))
        verdict = "PASS" if ok else "FAIL"
        detail = {"oracle_finals": finals, "mismatch_lines": len(mism)}
    else:
        named = [l for l in fails if l.startswith("FAIL: " + expected)]
        verdict = "KILLED" if (run_rc != 0 and named) else "SURVIVED"
        detail = {"expected": expected, "named": named[:4], "fail_lines": len(fails),
                  "first_fails": fails[:6]}
    return {"probe": name, "bench": bench, "mode": mode, "build_rc": build_rc,
            "run_rc": run_rc, "verdict": verdict, "secs": round(time.time() - t0),
            **detail}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    scratch = a.output.parent.parent / "scratch" / "tmp"
    scratch = Path(os.environ.get("R675_SCRATCH", scratch))
    scratch.mkdir(parents=True, exist_ok=True)
    chosen = [p for p in PROBES if not a.only or p[0] in a.only]
    results = []
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = {ex.submit(probe, p, a.tree.resolve(), a.output.resolve(),
                          a.verilator, scratch): p[0] for p in chosen}
        for f in cf.as_completed(futs):
            try:
                r = f.result()
            except Exception as e:  # recorded, never swallowed
                r = {"probe": futs[f], "verdict": "ERROR", "error": str(e)}
            print(json.dumps(r), flush=True)
            results.append(r)
    results.sort(key=lambda r: r["probe"])
    (a.output / "probes.json").write_text(json.dumps(results, indent=2) + "\n")
    good = all(r["verdict"] in ("KILLED", "PASS") for r in results)
    print("PROBES:", " ".join(f"{r['probe']}={r['verdict']}" for r in results))
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
