#!/usr/bin/env python3
"""Reviewer-owned plants at the merged head (disposable copies only).

Reuses the tree's own tb/pp_top/notify_mutants.py harness (copy_tree, plant,
execute, TALLY) so a probe is built and run exactly as a campaign arm, but the
defects are the reviewer's own, not the author's arms. Each probe states what it
expects:
  PASS              the run completes, exits 0, no FAIL line;
  FAIL:<p1>,<p2>..  the run completes, exits non-zero, and for every prefix pi at
                    least one FAIL line starts with it (a prefix may name one check
                    "WD2:" or a family "CA").
A refused edit, a failed build or a missing tally is never a kill.

usage: reviewer_probes.py TREE OUTDIR VERILATOR JOBS [NAME ...]
"""
import concurrent.futures
import re
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
VERILATOR = sys.argv[3]
JOBS = int(sys.argv[4])
ONLY = set(sys.argv[5:])

sys.path.insert(0, str(TREE / "tb/common"))
_spec = importlib.util.spec_from_file_location("nm", TREE / "tb/pp_top/notify_mutants.py")
nm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nm)
Suite = nm.Suite

TOP = "hdl/top/protocol_processor_top.sv"
NTFY = "hdl/aecp/KL_aecp_notify.sv"
BENCH = "tb/pp_top/sim_main.cpp"
WITHDRAW = Suite("tb/pp_top", ("make", "gsi-build"), ("./obj_dir/Vpp_top_sim", "--withdraw-only"))
INDEX = Suite("tb/aecp_notify", (), ("make", "run"))
INTERFACES = Suite("tb/aecp_notify", (), ("make", "interfaces"))
IF_TOP = Suite("tb/pp_top", ("make", "interfaces-build"), ("./obj_if2/Vpp_top_if2",))
FULL = Suite("tb/pp_top", ("make", "gsi-build"), ("./obj_dir/Vpp_top_sim",))

LANE0 = "                                   && org_withdraw_mask_r[laneq_org_r[0]];\n"
LANEI = "          && !org_withdraw_mask_r[laneq_org_r[i]]) begin\n"
ABORT = "  assign arb_start_abort_w = org_withdraw_mask_r[ser_slot_w]\n"
STAGE = ("    if (!rst_n) org_withdraw_mask_r <= '0;\n"
         "    else        org_withdraw_mask_r <= org_withdraw_slot_mask_w;\n")
DECL = "  logic [7:0]              org_withdraw_mask_r;\n"


def comb(line: str) -> tuple[str, str, str]:
    return (TOP, line, line.replace("org_withdraw_mask_r", "org_withdraw_slot_mask_w"))


def dropped(line: str) -> tuple[str, str, str]:
    """the reader sees no withdraw mask at all (only the release term remains)"""
    return (TOP, line, re.sub(r"org_withdraw_mask_r\[[^]]*\]\]?", "1'b0", line))


# the seventh (two-interface) top build runs section WD after section IF
IF2_WD = (BENCH, "  run_interfaces(h);\n  const char* const build = \"interfaces\";\n",
          "  run_interfaces(h);\n  run_withdraw(h);\n  const char* const build = \"interfaces\";\n")

CA_REQ = "  always_comb begin : ca_request\n"
LATE = ("  logic               rv_late_r;\n"
        "  always_ff @(posedge clk_i) rv_late_r <= ca_cancel_ok_w;\n" + CA_REQ)
OWN_CX = "    assign cx_ok_w   = ca_cancel_ok_w\n"
CK_OLD = ("            && (!ctr_sent_r[c]\n"
          "                || ((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin\n")
AV1 = "(((N_IF_P > 1) && (c == N_CTR_DESC_C - 1)) ? (N_STREAM_IN_P + N_STREAM_OUT_P) : c)"
CK_NEW = (f"            && (!ctr_sent_r[{AV1}]\n"
          f"                || ((now_ms_i - ctr_last_r[{AV1}]) >= 32'd1000))) begin\n")

PROBES = [
    # controls: the unplanted head
    ("ctl-withdraw", WITHDRAW, (), "PASS"),
    ("ctl-index", INDEX, (), "PASS"),
    ("ctl-interfaces", INTERFACES, (), "PASS"),
    ("ctl-if-top", IF_TOP, (), "PASS"),
    # #163 side, graded by WD (the top) and CX (tb/aecp_notify)
    ("r-wd-abort-only-comb", WITHDRAW, (comb(ABORT),), "FAIL:WD"),
    ("r-wd-lane-only-comb", WITHDRAW, (comb(LANE0), comb(LANEI)), "FAIL:WD"),
    ("r-wd-two-clocks", WITHDRAW, (
        (TOP, DECL, DECL + "  logic [7:0]              rv_wd_pre_r;\n"),
        (TOP, STAGE, "    if (!rst_n) begin org_withdraw_mask_r <= '0; rv_wd_pre_r <= '0; end\n"
                     "    else begin rv_wd_pre_r <= org_withdraw_slot_mask_w;"
                     " org_withdraw_mask_r <= rv_wd_pre_r; end\n")), "FAIL:WD"),
    ("r-wd-sticky", WITHDRAW, (
        (TOP, STAGE, "    if (!rst_n) org_withdraw_mask_r <= '0;\n"
                     "    else if (|org_withdraw_slot_mask_w) org_withdraw_mask_r <= org_withdraw_slot_mask_w;\n"),),
     "FAIL:WD"),
    ("r-cx-repeated", INDEX, (
        (NTFY, CA_REQ, LATE),
        (NTFY, OWN_CX, "    assign cx_ok_w   = rv_late_r || ca_cancel_ok_w\n")), "FAIL:CX1:"),
    # #69 side, graded by CA, PD and CK (tb/aecp_notify's third build)
    ("r-ca-settle-one", INTERFACES, (
        (NTFY, "    localparam logic [1:0] CX_SETTLE_C = 2'd3;\n",
         "    localparam logic [1:0] CX_SETTLE_C = 2'd1;\n"),), "FAIL:CA4"),
    ("r-ca-turns-ignore-pending-cancel", INTERFACES, (
        (NTFY, "          if (ca_probe_r[(i / N_IF_P) * N_IF_P + p] || cx_pend_r[(i / N_IF_P) * N_IF_P + p])\n",
         "          if (ca_probe_r[(i / N_IF_P) * N_IF_P + p])\n"),), "FAIL:CA"),
    ("r-ca-drain-cancel-dropped", INTERFACES, (
        (NTFY, "      if ((n_st_r == N_DRAIN) && ca_probe_r[pd_ix_w]) cx_work_w[pd_ix_w] = 1'b1;\n",
         ""),), "FAIL:CA"),
    ("r-ca-owner-low-bits", INTERFACES, (
        (NTFY, "    ca_owner_o    = 4'(ca_pick_ix_w[CIX_W_C-1 -: OIX_W_C]);\n",
         "    ca_owner_o    = 4'(ca_pick_ix_w[OIX_W_C-1:0]);\n"),
        (NTFY, "    ca_cancel_owner_o = 4'(cx_ix_w[CIX_W_C-1 -: OIX_W_C]);\n",
         "    ca_cancel_owner_o = 4'(cx_ix_w[OIX_W_C-1:0]);\n")), "FAIL:CA"),
    ("r-pd-any-port-row", INTERFACES, (
        (NTFY, "    assign wk_port_ok_w = (PORT_W_C'(wk_ix_r) == hold_port_r);\n",
         "    assign wk_port_ok_w = 1'b1;\n"),), "FAIL:PD"),
    ("r-ck-avb1-shares-avb0-window", INTERFACES, ((NTFY, CK_OLD, CK_NEW),), "FAIL:CK"),
    # is the registered mask itself graded? delayed two clocks / removed, against
    # section WD and against the whole default build (every section)
    ("r-wd-mask-dropped", WITHDRAW, (dropped(LANE0), dropped(LANEI), dropped(ABORT)), "FAIL:WD"),
    ("r-full-mask-dropped", FULL, (dropped(LANE0), dropped(LANEI), dropped(ABORT)), "FAIL:"),
    ("r-full-two-clocks", FULL, (
        (TOP, DECL, DECL + "  logic [7:0]              rv_wd_pre_r;\n"),
        (TOP, STAGE, "    if (!rst_n) begin org_withdraw_mask_r <= '0; rv_wd_pre_r <= '0; end\n"
                     "    else begin rv_wd_pre_r <= org_withdraw_slot_mask_w;"
                     " org_withdraw_mask_r <= rv_wd_pre_r; end\n")), "FAIL:"),
    # both sides at once: WD in the two-interface top build
    ("ctl-if-top-with-wd", IF_TOP, (IF2_WD,), "PASS"),
    ("r-if-top-wd-unregistered", IF_TOP, (IF2_WD, comb(LANE0), comb(LANEI), comb(ABORT)),
     "FAIL:WD1:,WD2:"),
]


def run(probe) -> dict:
    name, suite, edits, expect = probe
    with tempfile.TemporaryDirectory(prefix="rv-probe-") as temp:
        tree = Path(temp)
        nm.copy_tree(TREE, tree, suite)
        refusal = nm.plant(tree, edits)
        log = OUT / f"{name}.log"
        log.write_text("")
        if refusal:
            return {"probe": name, "expect": expect, "verdict": "REFUSED", "reason": refusal}
        cwd = tree / suite.directory
        build_rc = nm.execute(suite.build, cwd, log, VERILATOR) if suite.build else 0
        run_rc = nm.execute(suite.run, cwd, log, VERILATOR) if build_rc == 0 else None
    text = log.read_text(errors="replace")
    fails = [ln[len("FAIL: "):] for ln in text.splitlines() if ln.startswith("FAIL: ")]
    tallies = [m.group(0) for m in nm.TALLY.finditer(text)]
    completed = bool(tallies)
    if expect == "PASS":
        verdict = "PASS" if (run_rc == 0 and completed and not fails) else "UNEXPECTED"
        missing = []
    else:
        prefixes = expect[len("FAIL:"):].split(",")
        missing = [p for p in prefixes if not any(f.startswith(p) for f in fails)]
        verdict = ("KILLED" if (run_rc not in (0, None) and completed and not missing)
                   else "SURVIVED")
    return {"probe": name, "suite": " ".join(suite.run), "edits": len(edits), "expect": expect,
            "build_rc": build_rc, "run_rc": run_rc, "tallies": tallies, "missing": missing,
            "failing_checks": fails, "verdict": verdict}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    chosen = [p for p in PROBES if not ONLY or p[0] in ONLY]
    records = []
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        for rec in pool.map(run, chosen):
            records.append(rec)
            print(json.dumps({k: rec.get(k) for k in ("probe", "verdict", "missing", "tallies")}),
                  flush=True)
    (OUT / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    good = all(r["verdict"] in ("PASS", "KILLED") for r in records)
    print(f"reviewer probes: {sum(r['verdict'] in ('PASS', 'KILLED') for r in records)} of "
          f"{len(records)} as expected")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
