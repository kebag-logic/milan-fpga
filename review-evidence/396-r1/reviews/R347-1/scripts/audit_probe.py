#!/usr/bin/env python3
"""R347-1 probe: plan defects outside the shipped negative controls.

Usage: python3 -B audit_probe.py <extracted-tree>

Plants release-plan defects the shipped self-test and behave controls never
plant (second repeat group, peer side, outbound direction, talker side) and
grades each with (a) the reviewed audit and (b) each surviving audit mutant
from mutants.py.  A defect the reviewed audit rejects but a mutant accepts is
behaviour no shipped test pins.  Also probes parameter threading that the
shipped tests pin only at values equal to the defaults.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutants import MUTANTS  # noqa: E402


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def drop_target(step, entity, descriptor, index):
    step.args["counter_targets"] = [
        t for t in step.args["counter_targets"]
        if not (t["entity"] == entity and t["descriptor"] == descriptor
                and t["index"] == index)]


def defects(tp):
    dut, peer = tp.ARTY, tp.PEER
    out = []

    def case(name, area, sid, fn):
        plan = deepcopy(tp.build_plan(["matrix", "soak", "power"]))
        step = next(s for s in plan if s.sid == sid)
        fn(step)
        out.append((name, area, plan))

    case("D1 power.journal_commit misses DUT stream_input 1", "power",
         "power.journal_commit",
         lambda s: drop_target(s, dut.entity_id, "stream_input", 1))
    case("D2 power.journal_commit misses peer stream_input 2", "power",
         "power.journal_commit",
         lambda s: drop_target(s, peer.entity_id, "stream_input", 2))
    case("D3 power.journal_commit misses DUT stream_output 3", "power",
         "power.journal_commit",
         lambda s: drop_target(s, dut.entity_id, "stream_output", 3))
    case("D4 soak loses the outbound (DUT->peer) direction", "soak",
         "soak.continuous",
         lambda s: s.args.__setitem__("pairs", [
             p for p in s.args["pairs"] if p["talker"] != dut.entity_id]))
    case("D5 power.idle loses the outbound CRF pair", "power", "power.idle",
         lambda s: s.args.__setitem__("pairs", [
             p for p in s.args["pairs"]
             if not (p["talker"] == dut.entity_id
                     and p["talker_index"] == dut.crf_out)]))
    case("D6 power.journal_commit loses the return CRF pair", "power",
         "power.journal_commit",
         lambda s: s.args.__setitem__("pairs", [
             p for p in s.args["pairs"]
             if not (p["listener"] == dut.entity_id
                     and p["listener_index"] == dut.crf_in)]))
    return out


def grade(tp, plans):
    return [not tp.area_covers_every_index(plan, area)[0]
            for _, area, plan in plans]


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    src = tree / "tb/tools/torture_campaign.py"
    real = load(src, "tc_real")
    plans = defects(real)
    real_verdicts = grade(real, plans)
    print("reviewed audit (True = defect rejected):")
    for (name, _, _), v in zip(plans, real_verdicts):
        print(f"  {'REJECTS' if v else 'ACCEPTS'}  {name}")
    text = src.read_text()
    with tempfile.TemporaryDirectory() as tmp:
        for i, (name, old, new) in enumerate(MUTANTS):
            if not name.startswith("A") or "control" in name:
                continue
            path = Path(tmp) / f"tc_m{i}.py"
            path.write_text(text.replace(old, new))
            mod = load(path, f"tc_m{i}")
            verdicts = grade(mod, defects(mod))
            missed = [plans[j][0].split()[0] for j, v in enumerate(verdicts)
                      if real_verdicts[j] and not v]
            print(f"{name}: accepts {missed or 'none'} that the reviewed audit rejects")
    # parameter threading at non-default values
    s = real.ReleaseSettings(soak_duration_s=3600, soak_interval_s=300,
                             power_cycles=10, idle_cycles=8, commit_cycles=2)
    soak, idle, commit = real.build_plan(["soak", "power"], release=s)
    print("non-default threading:",
          {"interval_s": soak.args["interval_s"],
           "total_cycles": idle.args["total_cycles"],
           "cycles": [idle.args["cycles"], commit.args["cycles"]]})
    odd = real.ReleaseSettings(power_cycles=200, idle_cycles=199, commit_cycles=1)
    print("200 cuts split 199/1 release_eligible:",
          [x.args["release_eligible"] for x in real.build_plan(["power"], release=odd)])
    wide = real.ReleaseSettings(soak_interval_s=604800)
    print("7-day soak sampled only at the endpoints release_eligible:",
          real.build_plan(["soak"], release=wide)[0].args["release_eligible"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
