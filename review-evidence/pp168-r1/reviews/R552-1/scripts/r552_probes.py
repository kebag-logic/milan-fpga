#!/usr/bin/env python3
"""Reviewer fault probes for PR #171 (issue #168), graded with the repository's own
ACMP campaign machinery (tb/pp_top/acmp_mutants.py: isolated tree copies, golden first,
a probe is KILLED only when it builds, completes with a tally and exits non-zero).

Usage: python3 r552_probes.py REPO OUTPUT VERILATOR JOBS
Every probe edits a private copy; REPO is never written.
"""
import concurrent.futures
import json
import sys
from pathlib import Path

repo, output, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(repo / "tb" / "pp_top"))
import acmp_mutants as am  # noqa: E402  (the subject repository's own driver)

L = "hdl/acmp/KL_pp_acmp_listener.sv"
T = "hdl/top/protocol_processor_top.sv"
LISTENER = am.Suite("tb/acmp_listener", (), ("make", "run"))
TOP_ALL = am.Suite("tb/pp_top", ("make", "gsi-build"), ("./obj_dir/Vpp_top_sim",))

PROBES = [
    # P1: the published record leaks the private probe-controller overlay
    ("published_mask_removed", LISTENER,
     ((L, "      published_rec_w.settled_stream_id = 64'd0;\n", ""),)),
    ("published_mask_removed", TOP_ALL,
     ((L, "      published_rec_w.settled_stream_id = 64'd0;\n", ""),)),
    # P2: A5 no longer saves the sent controller into the private word
    ("overlay_write_removed", LISTENER,
     ((L, "                rec_r.settled_stream_id <= rec_r.bind_ctlr_eid;\n", ""),)),
    # P3: guard always reads the private word (state selection removed)
    ("guard_select_always_private", LISTENER,
     ((L, "((rec_r.sm_state == 3'(LSM_PWR))\n                               || (rec_r.sm_state == 3'(LSM_PW2)))",
       "1'b1"),)),
    ("guard_select_always_private", TOP_ALL,
     ((L, "((rec_r.sm_state == 3'(LSM_PWR))\n                               || (rec_r.sm_state == 3'(LSM_PW2)))",
       "1'b1"),)),
    # P4: GET_STREAM_INFO selector 6 VLAN not gated on PROBING_COMPLETED
    ("gsi_vlan_settle_gate_removed", TOP_ALL,
     ((T, "\n             && (gsi_status_w[7:5] == pp_acmp_pkg::PB_COMPLETED_C))", ")"),)),
    # P5: last controller octet falls outside the selection window
    ("ctlr_window_short", LISTENER,
     ((L, "(bidx_r < 6'd20)", "(bidx_r < 6'd19)"),)),
    # P6: A5 never clears status (BIND_NEW/TK paths keep a stale status)
    ("a5_status_never_cleared", LISTENER,
     ((L, "                if (evt_r != LEV_TMR_DELAY) rec_r.acmpsta <= 5'd0;\n", ""),)),
    # P7: A12 never clears status
    ("a12_status_never_cleared", LISTENER,
     ((L, "                if (evt_r != LEV_TMR_RETRY) rec_r.acmpsta <= 5'd0;\n", ""),)),
    # P8: the parent VID output takes the stored value's upper bits when they are set
    ("parent_vid_saturates", TOP_ALL,
     ((T, "bound_vlan_r[v][11:0];", "(|bound_vlan_r[v][15:12]) ? 12'hFFF : bound_vlan_r[v][11:0];"),)),
    # P9: SRP listener service receives the upper VLAN nibble instead of the VID
    ("srp_vid_from_upper_bits", TOP_ALL,
     ((T, "vid:   lstn_act_settle_vlan_w[11:0],", "vid:   {lstn_act_settle_vlan_w[15:12], lstn_act_settle_vlan_w[7:0]},"),)),
]


def main() -> int:
    output.mkdir(parents=True, exist_ok=True)
    work = (repo, output, verilator)
    suites = {(s.directory, s.run): s for _, s, _ in PROBES}
    records = [am.judge(am.golden_label(s), s, (), (), work) for _, s in sorted(suites.items())]
    for r in records:
        print(json.dumps({k: r[k] for k in ("mutant", "verdict")}), flush=True)
    if all(r["verdict"] == "PASS" for r in records):
        with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
            futs = [pool.submit(am.judge, f"{n}@{Path(s.directory).name}{''.join(a for a in s.run if a.startswith('--'))}",
                                s, e, (), work) for n, s, e in PROBES]
            for f in concurrent.futures.as_completed(futs):
                r = f.result()
                r["first_failures"] = r.get("failing_checks", [])[:12]
                r["failure_count"] = len(r.get("failing_checks", []))
                r.pop("failing_checks", None)
                records.append(r)
                print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "build_rc", "run_rc", "failure_count")}), flush=True)
    (output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    goldens_ok = all(r["verdict"] == "PASS" for r in records if r["mutant"].startswith("golden-"))
    print(f"R552 probes: goldens {'PASS' if goldens_ok else 'BROKEN'}; "
          + ", ".join(f"{r['mutant']}={r['verdict']}" for r in records if not r["mutant"].startswith("golden-")))
    return 0 if goldens_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
