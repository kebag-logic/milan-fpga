#!/usr/bin/env python3
"""R347-2 behavioural probe of the round-2 release contract.

Usage: python3 -B probe_r2.py <extracted-tree>

Imports tb/tools/torture_campaign.py from the extracted tree (never the
reviewed clone) and prints, for each case, what the planner emits.  Nothing
is asserted here; REPORT.md interprets the output.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

DUT = ("entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,"
       "crf_out=2,crf_in=2")
PEER = ("entity=8899aabbccddeeff,mac=8899aabbccdd,talker_index_set=0|2,"
        "listener_index_set=0|2,crf_out=3,crf_in=3")


def load(path: Path):
    spec = importlib.util.spec_from_file_location("tc_probe", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tc_probe"] = mod
    spec.loader.exec_module(mod)
    return mod


def cli(tree: Path, *args: str) -> tuple[int, str, str]:
    r = subprocess.run([sys.executable, "-B", "tb/tools/torture_campaign.py", *args],
                       cwd=tree, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    tp = load(tree / "tb/tools/torture_campaign.py")
    base = tp.ReleaseSettings(topology_explicit=True)

    print("== release_eligible [soak, power.idle, power.journal_commit] via API")
    for label, changes in (
            ("decided profile, explicit topology", {}),
            ("restore_bound_s relaxed to 3600", {"restore_bound_s": 3600}),
            ("restore_bound_s relaxed to 31", {"restore_bound_s": 31}),
            ("restore_bound_s tightened to 10", {"restore_bound_s": 10}),
            ("boot_margin_s 1", {"boot_margin_s": 1}),
            ("boot_margin_s 600", {"boot_margin_s": 600}),
            ("soak_interval_s 61 (power judged on the soak cadence)", {"soak_interval_s": 61})):
        plan = tp.build_plan(["soak", "power"], release=replace(base, **changes))
        extra = {k: plan[1].args[k] for k in ("restore_bound_s", "boot_observation_s")}
        print(f"  {label}: {[s.args['release_eligible'] for s in plan]} {extra}")

    print("== release_eligible via CLI with both explicit specs")
    for flags in ([], ["--restore-bound-s", "3600"], ["--restore-bound-s", "3600", "--boot-margin-s", "1"]):
        rc, out, err = cli(tree, "--plan", "--areas", "soak,power", "--json",
                           "--dut", DUT, "--peer", PEER, *flags)
        steps = json.loads(out) if rc == 0 else []
        print(f"  flags {flags or 'none'}: rc {rc}; release_eligible "
              f"{[s['args']['release_eligible'] for s in steps]}; restore_bound_s "
              f"{[s['args'].get('restore_bound_s') for s in steps]}")

    print("== CRF/AAF overlap refusal (round-1 S2)")
    for spec in ("talker_index_set=0|1|4,crf_out=4", "listener_index_set=0|4,crf_in=4",
                 "talkers=5,crf_out=2", "listeners=5,crf_in=2"):
        rc, _, err = cli(tree, "--plan", "--areas", "soak,power", "--json", "--dut", spec)
        print(f"  --dut {spec}: rc {rc}; {err}")
    rc, _, err = cli(tree, "--plan", "--areas", "matrix", "--json", "--dut",
                     "talker_index_set=0|1|4,crf_out=4")
    print(f"  matrix-only with the overlapping spec: rc {rc}; {err}")

    print("== topology_explicit from CLI specs")
    for label, flags in (("dut spec without mac", ["--dut", DUT.replace("mac=001122334455,", ""), "--peer", PEER]),
                         ("peer spec without listeners", ["--dut", DUT, "--peer", PEER.replace("listener_index_set=0|2,", "")]),
                         ("empty value for entity", ["--dut", DUT.replace("entity=0011223344556677", "entity="), "--peer", PEER])):
        rc, out, err = cli(tree, "--plan", "--areas", "power", "--json", *flags)
        val = [s["args"]["topology_explicit"] for s in json.loads(out)] if rc == 0 else err
        print(f"  {label}: rc {rc}; topology_explicit {val}")

    print("== check_release_boot")
    for args, kw in (((1, 0), {"capture_complete": True}), ((2, 1), {"capture_complete": True}),
                     ((1, 1), {"capture_complete": True}), ((0, 0), {"capture_complete": True}),
                     ((1, 0), {"capture_complete": 1}), ((1, 0), {"capture_complete": False}),
                     ((None, None), {"capture_complete": True})):
        print(f"  check_release_boot{args}, {kw}: {tp.check_release_boot(*args, **kw)[0]}")

    print("== ADP window arithmetic implied by the plan formula (DUT valid_time=10 per Milan 5.6.2)")
    unit = tp.build_plan(["power"])[0].args["adp_valid_time_unit_s"]
    for since_last_adp, off_s in ((0, 2), (5, 2), (5, 10), (5, 15), (0, 20)):
        deadline = -since_last_adp - off_s + unit * 10  # host times relative to the cut
        print(f"  cut {since_last_adp} s after last ADP, T0 {off_s} s after cut: "
              f"adp_deadline {deadline} s after T0")
    return 0


if __name__ == "__main__":
    with contextlib.redirect_stderr(io.StringIO()):
        pass
    sys.exit(main())
