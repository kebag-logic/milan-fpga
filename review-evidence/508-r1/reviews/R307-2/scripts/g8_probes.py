#!/usr/bin/env python3
"""Reviewer probes for PR #560 G8: plant one processor-copy edit through the
suite's own gsi_mutants.py machinery (same recipe, same verdict reader), run
the timed obj_notify leg, and print every [GSI] G8 line plus the tally.
Usage: g8_probes.py <repo> <workdir> [probe ...]"""
import importlib.util, sys
from pathlib import Path
repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("gm", repo / "tb/verilator/milan_dp/gsi_mutants.py")
gm = importlib.util.module_from_spec(spec); spec.loader.exec_module(gm)
UNREG = "          || srp_evt_tk_reg_w[k] || srp_evt_tk_unreg_w[k]"
TEAR = "          || lstn_gsi_changed_r[k]\n          || srp_evt_tk_reg_w[k]"
PROBES = {
    # the registrar-withdrawal term leaves stri_events
    "P1_no_unreg_term": [("pp", UNREG, "          || srp_evt_tk_reg_w[k]")],
    # the settlement (pbsta/acmpsta commit) term leaves stri_events
    "P2_no_settle_term": [("pp", TEAR, "          || srp_evt_tk_reg_w[k]")],
}
work.mkdir(parents=True, exist_ok=True)
names = sys.argv[3:] or list(PROBES)
for name in names:
    planted = gm.plant(name, PROBES[name], work, name)
    assert planted, name
    exe = gm.build(planted[0], planted[1], work / f"obj_{name}")
    assert exe, f"{name} did not build"
    rc, out = gm.run_leg(exe)
    (work.parent / f"probe_{name}.log").write_text(out)
    print(f"===== {name}: rc={rc} verdict={gm.verdict(rc, out, None)} ({gm.log_reports_failure(out)[0]})")
    for ln in out.splitlines():
        if "G8" in ln or ln.startswith("checks:"):
            print("   ", ln)
    fails = [ln for ln in out.splitlines() if "[FAIL]" in ln or ln.strip().startswith("[FAIL")]
    print(f"    ({len(fails)} [FAIL] lines; first 12:)")
    for ln in fails[:12]:
        print("   ", ln)
