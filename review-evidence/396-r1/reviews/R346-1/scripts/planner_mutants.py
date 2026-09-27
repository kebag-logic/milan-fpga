#!/usr/bin/env python3
"""R346-1 probe: source mutants of tb/tools/torture_campaign.py, each graded by
the head's own gates (planner --self-test and the plan feature under behave).

Usage: python3 -B planner_mutants.py <repo-root> <scratch-dir>
A pristine copy of tb/tools, tests and scripts is exported from HEAD with
`git archive` into <scratch-dir>/base; each mutant runs in its own copy.
Killed = at least one gate exits non-zero.  The repository is never written.
"""
from __future__ import annotations

import concurrent.futures as cf
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
base = scratch / "base"
PLANNER = "tb/tools/torture_campaign.py"

M = {
    # ---- generator: coverage omissions
    "G01 soak/power targets drop DUT listener 1":
        ("                           for index in indices)\n    return targets",
         "                           for index in indices if not (device is dut and "
         "descriptor == 'stream_input' and index == 1))\n    return targets"),
    "G02 targets drop DUT CRF sink":
        ("                           for index in indices)\n    return targets",
         "                           for index in indices if not (device is dut and "
         "descriptor == 'stream_input' and index == crf_index))\n    return targets"),
    "G03 targets drop peer CRF sink":
        ("                           for index in indices)\n    return targets",
         "                           for index in indices if not (device is peer and "
         "descriptor == 'stream_input' and index == crf_index))\n    return targets"),
    "G04 targets drop DUT CRF output":
        ("                           for index in indices)\n    return targets",
         "                           for index in indices if not (device is dut and "
         "descriptor == 'stream_output' and index == crf_index))\n    return targets"),
    "G05 pairs outbound direction only":
        ("    for talker, listener in ((dut, peer), (peer, dut)):\n        outputs",
         "    for talker, listener in ((dut, peer),):\n        outputs"),
    "G06 pairs omit return CRF pair":
        ("        pairs.append(_multi_pair(Endpoint(talker, talker.crf_out),",
         "        if talker is dut: pairs.append(_multi_pair(Endpoint(talker, talker.crf_out),"),
    "G07 commit repeat drops DUT listener 1 target":
        ("        args = _release_args(dut, peer)\n        args.update(cycles=count,",
         "        args = _release_args(dut, peer)\n        if phase == 'journal_commit':\n"
         "            args['counter_targets'] = [t for t in args['counter_targets'] if not "
         "(t['entity'] == dut.entity_id and t['descriptor'] == 'stream_input' and t['index'] == 1)]\n"
         "        args.update(cycles=count,"),
    "G08 commit repeat drops return direction":
        ("        args = _release_args(dut, peer)\n        args.update(cycles=count,",
         "        args = _release_args(dut, peer)\n        if phase == 'journal_commit':\n"
         "            args['pairs'] = [p for p in args['pairs'] if p['talker'] != peer.entity_id]\n"
         "        args.update(cycles=count,"),
    "G09 power emits idle phase only":
        ("    for phase, count in ((\"idle\", settings.idle_cycles),\n"
         "                         (\"journal_commit\", settings.commit_cycles)):",
         "    for phase, count in ((\"idle\", settings.idle_cycles),):"),
    "G10 CRF output bound to AAF sink":
        ("        outputs = talker.talker_indices(include_crf=False)",
         "        outputs = talker.talker_indices(include_crf=True)"),
    # ---- generator: parameters hardcoded or dropped
    "P01 soak interval hardcoded 60":
        ("interval_s=settings.soak_interval_s,", "interval_s=60,"),
    "P02 soak duration hardcoded 604800":
        ("args.update(duration_s=settings.soak_duration_s,", "args.update(duration_s=604800,"),
    "P03 total cycles hardcoded 200":
        ("total_cycles=settings.power_cycles,", "total_cycles=200,"),
    "P04 idle count hardcoded 160":
        ("((\"idle\", settings.idle_cycles),", "((\"idle\", 160),"),
    "P05 commit count hardcoded 40":
        ("(\"journal_commit\", settings.commit_cycles)):", "(\"journal_commit\", 40)):"),
    "P06 persisted items hardcoded":
        ("persisted_items=list(settings.persisted_items),", "persisted_items=[\"stream_binding\"],"),
    "P07 CLI ignores --soak-interval-s":
        ("release = ReleaseSettings(a.soak_duration_s, a.soak_interval_s,",
         "release = ReleaseSettings(a.soak_duration_s, ReleaseSettings.soak_interval_s,"),
    "P08 CLI ignores --soak-duration-s":
        ("release = ReleaseSettings(a.soak_duration_s, a.soak_interval_s,",
         "release = ReleaseSettings(ReleaseSettings.soak_duration_s, a.soak_interval_s,"),
    "P09 CLI ignores --persisted-items":
        ("tuple(a.persisted_items.split(\",\")))", "ReleaseSettings.persisted_items)"),
    # ---- generator: contract values
    "C01 snapshot policies swapped":
        ("snapshot_policy=(\"complete old or new committed snapshot\"\n"
         "                                     if phase == \"journal_commit\"",
         "snapshot_policy=(\"complete old or new committed snapshot\"\n"
         "                                     if phase != \"journal_commit\""),
    "C02 commit cut not tied to commit window":
        ("cut_requires=(\"journal_commit_window\" if phase == \"journal_commit\"",
         "cut_requires=(\"journal_commit_window\" if phase == \"never\""),
    "C03 rebind limit 2 s":
        ("rebind_limit_s=1,", "rebind_limit_s=2,"),
    "C04 rebind limit inclusive":
        ("rebind_limit_exclusive=True,", "rebind_limit_exclusive=False,"),
    "C05 resets counted":
        ("cold=True, count_resets=False,", "cold=True, count_resets=True,"),
    "C06 warm cuts":
        ("cold=True, count_resets=False,", "cold=False, count_resets=False,"),
    "C07 soak release_eligible always true":
        ("release_eligible=(settings.soak_duration_s\n"
         "                                  >= ReleaseSettings.soak_duration_s),",
         "release_eligible=True,"),
    "C08 power eligibility ignores commit count":
        ("\n                                      and settings.commit_cycles >= ReleaseSettings.commit_cycles),",
         "),"),
    "C09 crf flag never set":
        ("\"crf\": index == crf_index}", "\"crf\": False}"),
    "C10 no endpoint sample":
        ("sample_at_start=True, sample_at_end=True,", "sample_at_start=True, sample_at_end=False,"),
    "C11 TSD register offset wrong":
        ("\"offset\": 0x6EC,", "\"offset\": 0x6E8,"),
    "C12 uptime assertion dropped":
        ("    AssertSpec(\"soak.uptime-monotonic\", RELEASE_CLAUSE +",
         "    ) and None or (AssertSpec(\"soak.uptime-monotonic\", RELEASE_CLAUSE +"),
    "C13 boot observation 60 s":
        ("boot_observation_s=480,", "boot_observation_s=60,"),
    "C14 needs_human false on power":
        ("asserts=POWER_ASSERTS, clause=RELEASE_CLAUSE, needs_human=True,",
         "asserts=POWER_ASSERTS, clause=RELEASE_CLAUSE, needs_human=False,"),
    # ---- settings validation
    "V01 phase sum not enforced":
        ("        if self.idle_cycles + self.commit_cycles != self.power_cycles:",
         "        if False:"),
    "V02 interval > duration allowed":
        ("        if self.soak_interval_s > self.soak_duration_s:", "        if False:"),
    "V03 duplicate persisted items allowed":
        ("                or len(set(items)) != len(items)):", "                or False):"),
    # ---- audit
    "A01 audit ignores counter targets":
        ("            absent = sorted(set(indices) - seen)", "            absent = []"),
    "A02 audit checks outbound only":
        ("    for direction, talker, listener in ((\"outbound\", dut, peer),\n"
         "                                        (\"return\", peer, dut)):",
         "    for direction, talker, listener in ((\"outbound\", dut, peer),):"),
    "A03 audit drops CRF binding check":
        ("            missing[direction + \"_crf\"] = \"missing CRF binding\"", "            pass"),
    "A04 audit drops AAF binding check":
        ("            missing[direction] = \"missing AAF binding\"", "            pass"),
    "A05 audit only first repeat":
        ("        for step in steps:\n            defects", "        for step in steps[:1]:\n            defects"),
    "A06 audit drops phase check":
        ("        if area == \"power\" and {s.args.get(\"phase\") for s in steps} != {",
         "        if False and {s.args.get(\"phase\") for s in steps} != {"),
    "A07 release audit branch removed":
        ("    if area in (\"soak\", \"power\"):\n        steps = [s for s in plan if s.area == area]",
         "    if False:\n        steps = [s for s in plan if s.area == area]"),
    "A08 generic coverage ignores counter targets":
        ("        for target in a.get(\"counter_targets\", []):\n            for role, device",
         "        for target in []:\n            for role, device"),
}


def run(name: str, old: str, new: str) -> tuple[str, str, str]:
    work = scratch / ("m_" + name.split()[0])
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(base, work, symlinks=True)
    path = work / PLANNER
    text = path.read_text()
    if text.count(old) != 1:
        return name, "INVALID", f"anchor matches {text.count(old)} times"
    path.write_text(text.replace(old, new))
    res = []
    st = subprocess.run([sys.executable, "-B", PLANNER, "--self-test"], cwd=work,
                        capture_output=True, text=True, timeout=600)
    res.append(("self-test", st.returncode))
    bh = subprocess.run([sys.executable, "-B", "-m", "behave",
                         "tests/features/torture_campaign_plan.feature", "-f", "plain",
                         "--no-capture"], cwd=work, capture_output=True, text=True,
                        timeout=600)
    res.append(("behave", bh.returncode))
    shutil.rmtree(work)
    killed = [g for g, rc in res if rc != 0]
    return name, "KILLED" if killed else "SURVIVED", ",".join(killed) or "-"


if base.exists():
    shutil.rmtree(base)
base.mkdir(parents=True)
subprocess.run(f"git -C '{root}' archive HEAD tb/tools tests scripts | tar -x -C '{base}'",
               shell=True, check=True)
# the pristine copy must pass both gates, or no mutant verdict means anything
ok = run.__wrapped__ if hasattr(run, "__wrapped__") else None
pristine = subprocess.run([sys.executable, "-B", PLANNER, "--self-test"], cwd=base,
                          capture_output=True, text=True).returncode
pristine_b = subprocess.run([sys.executable, "-B", "-m", "behave",
                             "tests/features/torture_campaign_plan.feature", "-f", "plain"],
                            cwd=base, capture_output=True, text=True).returncode
print(f"pristine: self-test rc={pristine} behave rc={pristine_b}")
with cf.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(lambda kv: run(kv[0], *kv[1]), M.items()))
for name, verdict, how in results:
    print(f"{verdict:9s} {name:50s} {how}")
survived = [r for r in results if r[1] != "KILLED"]
print(f"{len(results)} mutants: {len(results) - len(survived)} killed, "
      f"{sum(r[1] == 'SURVIVED' for r in results)} survived, "
      f"{sum(r[1] == 'INVALID' for r in results)} invalid")
sys.exit(0)
