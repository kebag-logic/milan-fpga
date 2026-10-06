#!/usr/bin/env python3
"""Reviewer-owned disposable probes against tb/pp_top section DN (issue #42).

Reuses the tree's own tb/pp_top/notify_mutants.py machinery (Suite, Mutant, judge,
goldens) so a probe is graded exactly like an author control: KILLED only when the
copy builds, the run completes with its tally, exits non-zero, and every named check
fails. Probes marked EXPECT_SURVIVE document a stated limit, not a gap.

Usage: r502_probes.py TREE OUTPUT [--jobs N] [--verilator V]
"""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--verilator", default="verilator")
    a = ap.parse_args()
    tree = a.tree.resolve()
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("nm", tree / "tb/pp_top/notify_mutants.py")
    nm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nm)
    M, S, TOP, NTFY = nm.Mutant, nm.DOMAIN_NOTIFY_SUITE, nm.TOP, nm.NTFY
    DOM, OR = nm.SRP_DOMAIN, nm.AVB_OR
    EDGE = " || (link_up_i != link_q_r)"
    AVB_PICK = "      pick_dt_w   = 16'h0009;           // AVB_INTERFACE\n"
    probes = (
        M("r_link_rise_only", S, ((TOP, OR, OR.replace(EDGE, " || (link_up_i && !link_q_r)")),),
          ("DN4b:", "DN4c:")),
        M("r_link_fall_only", S, ((TOP, OR, OR.replace(EDGE, " || (!link_up_i && link_q_r)")),),
          ("DN4d:", "DN4e:")),
        M("r_link_level_down", S, ((TOP, OR, OR.replace(EDGE, " || !link_up_i")),),
          ("DN4b:",)),
        M("r_adopt_prio_only", S, ((DOM,
          "          && ({surf_prio_w, rxdom_vid_i} != {decl_prio_r, decl_vid_r})) begin\n",
          "          && (surf_prio_w != decl_prio_r)) begin\n"),),
          ("<bench-switch-model>:", "DN1b:", "DN1c:")),
        M("r_rejoin_strobes", S, ((DOM,
          "        rejoin_pend_r <= 1'b0;\n      end\n    end\n  end\n",
          "        rejoin_pend_r <= 1'b0;\n        evt_domain_change_o <= 1'b1;\n"
          "      end\n    end\n  end\n"),),
          ("DN3:", "DN3b:")),
        M("r_avb_index_1", S, ((NTFY, AVB_PICK, AVB_PICK + "      pick_di_w   = 16'd1;\n"),),
          ("DN4c:", "DN4e:", "DN1c:", "DN2c:")),
        # stated limit (README section DN): the LINK_DOWN revert's strobe is not
        # separable at ev_avb_i; DN starts at DEFAULTS, so this must survive DN
        M("r_EXPECT_SURVIVE_revert_no_strobe", S, ((DOM,
          "        if (adopted_r) evt_domain_change_o <= 1'b1;\n", ""),), ("DN",)),
    )
    work = (tree, out, a.verilator)
    records = [nm.judge(g, work) for g in nm.goldens(list(probes))]
    if all(r["verdict"] == "PASS" for r in records):
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
            for f in concurrent.futures.as_completed([pool.submit(nm.judge, p, work)
                                                      for p in probes]):
                records.append(f.result())
    (out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
    for r in records:
        print(json.dumps({k: r.get(k) for k in ("mutant", "verdict", "run_rc", "missing",
                                                "failing_checks")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
