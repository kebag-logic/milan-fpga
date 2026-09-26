#!/usr/bin/env python3
"""Reviewer-owned mutation campaign for the aecp_name_wr_o export (issue #120).

Each mutant is applied to a private copy of the head scratch tree (hdl,
tb/common, tb/pp_top), built with the pinned simulator and run with
--name-writes-only. Store-level mutants change ONLY the exported wire: the
name RAM enable is restored to its original expression, so the RAM behaviour
is unchanged and the wrapper's RAM-enable tap stays an independent observer.

Verdicts come from the completed simulation only (tally line present):
  KILLED   - simulation completed, returned non-zero, at least one FAIL line
  SURVIVED - simulation completed, returned zero, no FAIL line
  INVALID  - build failed or no tally line (never counted as detection)
Survivors are re-run through the full default build (every section).
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

STORE = "hdl/aecp/KL_aecp_desc_store.sv"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
TOP = "hdl/top/protocol_processor_top.sv"
S_ASSIGN = "  assign name_wr_o = take_wr_w && st_name_i;"
S_WE = "      name_we_w    = name_wr_o;"
S_WE_ORIG = "      name_we_w    = take_wr_w && st_name_i;"
E_CONN = "      .name_wr_o         (name_wr_o),"
E_ANCHOR = "  logic [15:0] store_fetch_nc_w, store_rowr_nc_w, store_dlen_nc_w;"
T_CONN = "      .name_wr_o          (aecp_name_wr_o),"
ACC = "(take_wr_w && st_name_i)"


def store(expr: str, extra: str = "") -> list[tuple[str, str, str]]:
    """Export-only store mutation: new name_wr_o expression, RAM enable unchanged."""
    return [(STORE, S_WE, S_WE_ORIG),
            (STORE, S_ASSIGN, extra + f"  assign name_wr_o = {expr};")]


def engine(expr: str) -> list[tuple[str, str, str]]:
    """Engine mutation: disconnect the store export and drive the port from `expr`."""
    return [(ENGINE, E_CONN, "      .name_wr_o         (),"),
            (ENGINE, E_ANCHOR, E_ANCHOR + f"\n  assign name_wr_o = {expr};")]


STICKY = ("  logic mut_lvl_r;\n  always_ff @(posedge clk_i) begin : mut_lvl\n"
          f"    if (!rst_n) mut_lvl_r <= 1'b0; else if {ACC} mut_lvl_r <= 1'b1;\n  end\n")
STRETCH = ("  logic mut_q_r;\n  always_ff @(posedge clk_i) begin : mut_q\n"
           f"    if (!rst_n) mut_q_r <= 1'b0; else mut_q_r <= {ACC};\n  end\n")
FIRSTONLY = ("  logic mut_seen_r;\n  always_ff @(posedge clk_i) begin : mut_seen\n"
             "    if (!rst_n) mut_seen_r <= 1'b0;\n"
             f"    else if {ACC} mut_seen_r <= 1'b1;\n"
             "    else if (st_req_i && !st_name_i) mut_seen_r <= 1'b0;\n  end\n")
ISSUE = ("  logic mut_iss_r;\n  always_ff @(posedge clk_i) begin : mut_iss\n"
         "    if (!rst_n) mut_iss_r <= 1'b0;\n"
         "    else mut_iss_r <= st_req_i && st_we_i && st_name_i && !st_ready_o;\n  end\n")

MUTANTS = {
    # command/µop decode instead of store acceptance
    "M01-cmd-decode-at-mark": engine("eff_nvm_stb_o && (eff_nvm_mark_o == 8'd7)"),
    "M02-uop-decode-request": engine("st_req_w && st_we_w && st_name_w"),
    "M03-uop-issue-first-cycle": store(
        "st_req_i && st_we_i && st_name_i && !mut_iss_r", ISSUE),
    "M04-request-not-ready-qualified": store("st_req_i && st_we_i && st_name_i"),
    # level / width
    "M05-sticky-level": store(f"{ACC} || mut_lvl_r", STICKY),
    "M06-two-cycle-stretch": store(f"{ACC} || mut_q_r", STRETCH),
    "M07-one-cycle-late": store("mut_q_r", STRETCH),
    # missing beats of a multi-lane name
    "M08-drop-lane0": store(f"{ACC} && (st_addr_i[5:3] != 3'd0)"),
    "M09-drop-lane7": store(f"{ACC} && (st_addr_i[5:3] != 3'd7)"),
    "M10-first-lane-per-command": store(f"{ACC} && !mut_seen_r", FIRSTONLY),
    # wrong qualification
    "M11-includes-boot-load": store(f"{ACC} || ((st_r == S_NAM_RSP) && beat_w)"),
    "M12-any-store-write": store("take_wr_w"),
    # top wiring
    "M14-top-tied-low": [(TOP, T_CONN, "      .name_wr_o          (),")],
}


def run(cmd: list[str], cwd: Path, log: Path) -> int:
    """Foreground run; stdout+stderr to `log`; return the exit status."""
    with log.open("w") as out:
        return subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT,
                              check=False).returncode


def verdict(log: Path, rc: int) -> tuple[str, list[str]]:
    """Grade one completed simulation from its own transcript."""
    text = log.read_text(errors="replace")
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    if "[build default," not in text:
        return "INVALID", fails
    if rc != 0 and fails:
        return "KILLED", fails
    if rc == 0 and not fails:
        return "SURVIVED", fails
    return "INVALID", fails


def main() -> int:
    """Apply, build, run and grade every mutant (plus golden)."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    pk = args.packet.resolve()
    src = pk / "scratch/head"
    out = pk / "receipts/05-reviewer-mutants"
    out.mkdir(parents=True, exist_ok=True)
    os.environ["PATH"] = f"{pk / 'tools'}:{os.environ['PATH']}"
    names = ["M00-golden"] + list(MUTANTS)
    if args.only:
        names = [n for n in names if n in args.only]
    results = []
    for name in names:
        tree = pk / "scratch/mut" / name
        shutil.rmtree(tree, ignore_errors=True)
        for d in ("hdl", "tb/common", "tb/pp_top"):
            shutil.copytree(src / d, tree / d,
                            ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
        # M14 needs an explicit driver for the undriven top output
        edits = MUTANTS.get(name, [])
        for path, old, new in edits:
            f = tree / path
            text = f.read_text()
            assert text.count(old) == 1, (name, path, old)
            f.write_text(text.replace(old, new))
        if name == "M14-top-tied-low":
            f = tree / TOP
            text = f.read_text()
            anchor = "endmodule"
            i = text.rindex(anchor)
            f.write_text(text[:i] + "  assign aecp_name_wr_o = 1'b0;\n" + text[i:])
        bench = tree / "tb/pp_top"
        brc = run(["make", "gsi-build"], bench, out / f"{name}-build.log")
        rrc, v, fails, full = None, "INVALID", [], None
        if brc == 0:
            log = out / f"{name}-nw.log"
            rrc = run(["./obj_dir/Vpp_top_sim", "--name-writes-only"], bench, log)
            v, fails = verdict(log, rrc)
            if v == "SURVIVED" and name != "M00-golden":
                flog = out / f"{name}-full.log"
                frc = run(["./obj_dir/Vpp_top_sim"], bench, flog)
                fv, ff = verdict(flog, frc)
                full = dict(rc=frc, verdict=fv, failures=ff[:20])
        diff = subprocess.run(["diff", "-ru", str(src / "hdl"), str(tree / "hdl")],
                              capture_output=True, text=True).stdout
        (out / f"{name}.diff").write_text(diff.replace(str(pk), "<packet>"))
        res = dict(mutant=name, build_rc=brc, run_rc=rrc, verdict=v,
                   failures=sorted(set(fails)), full_suite=full)
        results.append(res)
        print(json.dumps(dict(mutant=name, build_rc=brc, run_rc=rrc, verdict=v,
                              n_fail=len(fails),
                              full=None if full is None else full["verdict"])),
              flush=True)
        shutil.rmtree(tree / "tb/pp_top/obj_dir", ignore_errors=True)
    # merge with earlier chunks, keyed by mutant name, in campaign order
    merged = {}
    if (out / "results.json").exists():
        merged = {r["mutant"]: r for r in json.loads((out / "results.json").read_text())}
    merged.update({r["mutant"]: r for r in results})
    order = ["M00-golden"] + list(MUTANTS)
    results = [merged[n] for n in order if n in merged]
    (out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    golden_ok = any(r["mutant"] == "M00-golden" and r["verdict"] == "SURVIVED"
                    for r in results)
    print(f"golden passes: {golden_ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
