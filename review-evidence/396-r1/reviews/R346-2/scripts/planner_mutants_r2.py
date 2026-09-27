#!/usr/bin/env python3
"""R346-2 probe (round-2 code): source mutants of tb/tools/torture_campaign.py, each graded by
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
    # ---- timing parameters (decision 5854930205)
    "R01 restore bound hardcoded 30":
        ("                    restore_bound_s=settings.restore_bound_s,",
         "                    restore_bound_s=30,"),
    "R02 boot margin arg hardcoded 5":
        ("                    boot_margin_s=settings.boot_margin_s,",
         "                    boot_margin_s=5,"),
    "R03 observation omits margin":
        ("boot_observation_s=settings.restore_bound_s + settings.boot_margin_s,",
         "boot_observation_s=settings.restore_bound_s,"),
    "R04 observation hardcoded 35":
        ("boot_observation_s=settings.restore_bound_s + settings.boot_margin_s,",
         "boot_observation_s=35,"),
    "R05 CLI ignores --restore-bound-s":
        ("release = replace(release, restore_bound_s=a.restore_bound_s,",
         "release = replace(release, restore_bound_s=ReleaseSettings.restore_bound_s,"),
    "R06 CLI ignores --boot-margin-s":
        ("                          boot_margin_s=a.boot_margin_s,",
         "                          boot_margin_s=ReleaseSettings.boot_margin_s,"),
    "R07 restore bound not validated":
        ("\"idle_cycles\", \"commit_cycles\", \"restore_bound_s\", \"boot_margin_s\"):",
         "\"idle_cycles\", \"commit_cycles\", \"boot_margin_s\"):"),
    "R08 margin not validated":
        ("\"idle_cycles\", \"commit_cycles\", \"restore_bound_s\", \"boot_margin_s\"):",
         "\"idle_cycles\", \"commit_cycles\", \"restore_bound_s\"):"),
    "R09 restore bound not provisional":
        ("restore_bound_provisional=True,", "restore_bound_provisional=False,"),
    "R10 restore limit exclusive":
        ("restore_limit_exclusive=False,", "restore_limit_exclusive=True,"),
    "R11 ADP limit inclusive":
        ("adp_limit_exclusive=True,", "adp_limit_exclusive=False,"),
    "R12 ADP unit 1 s":
        ("adp_valid_time_unit_s=2,", "adp_valid_time_unit_s=1,"),
    "R13 ADP deadline literal":
        ("adp_deadline=\"pre_cut_last_available_host_s + 2 * pre_cut_valid_time - t0_host_s\",",
         "adp_deadline=\"62\","),
    "R14 rebind no longer after restore":
        ("rebind_requires=\"automatic restoration passed for every persisted binding\",",
         "rebind_requires=\"none\","),
    "R15 restore end first ADP":
        ("restore_end=\"first valid AVTP PDU of each persisted binding\",",
         "restore_end=\"first ENTITY_AVAILABLE\","),
    "R16 restore requires dropped CRF":
        ("restore_requires=\"automatic; no controller repair; both directions and CRF\",",
         "restore_requires=\"automatic\","),
    "R17 time origin network readiness":
        ("time_origin=\"T0: power-strip ON command, host monotonic clock\",",
         "time_origin=\"network readiness\","),
    "R18 automatic-restore assertion dropped":
        ("    AssertSpec(\"power.automatic-restore-bound\", RELEASE_CLAUSE +",
         "    ) and None or (AssertSpec(\"power.automatic-restore-bound\", RELEASE_CLAUSE +"),
    "R19 adp missing/expired policy weakened":
        ("adp_missing_or_expired=\"fail; never replace the pre-cut origin\",",
         "adp_missing_or_expired=\"skip\","),
    "R20 restore start not T0":
        ("                    restore_start=\"T0\",", "                    restore_start=\"ENTITY_AVAILABLE\","),
    # ---- eligibility (R346-1 F3)
    "E01 eligibility ignores topology":
        ("    return (settings.topology_explicit\n            and \"stream_binding\"",
         "    return (True\n            and \"stream_binding\""),
    "E02 eligibility ignores binding inventory":
        ("            and \"stream_binding\" in settings.persisted_items\n",
         "            and True\n"),
    "E03 eligibility ignores interval":
        ("            and settings.soak_interval_s <= RELEASE_MAX_SOAK_INTERVAL_S)",
         "            and True)"),
    "E04 interval ceiling exclusive":
        ("            and settings.soak_interval_s <= RELEASE_MAX_SOAK_INTERVAL_S)",
         "            and settings.soak_interval_s < RELEASE_MAX_SOAK_INTERVAL_S)"),
    "E05 interval ceiling 600":
        ("RELEASE_MAX_SOAK_INTERVAL_S = 60\n", "RELEASE_MAX_SOAK_INTERVAL_S = 600\n"),
    "E06 soak skips profile eligibility":
        ("    args[\"release_eligible\"] &= _release_profile_eligible(settings)\n    args[\"max_soak_interval_s\"]",
         "    args[\"max_soak_interval_s\"]"),
    "E07 power skips profile eligibility":
        ("        args[\"release_eligible\"] &= _release_profile_eligible(settings)\n        args[\"topology_explicit\"]",
         "        args[\"topology_explicit\"]"),
    "E08 explicit check ignores peer":
        ("    for spec in (dut_spec, peer_spec):\n        keys", "    for spec in (dut_spec,):\n        keys"),
    "E09 explicit check ignores dut":
        ("    for spec in (dut_spec, peer_spec):\n        keys", "    for spec in (peer_spec,):\n        keys"),
    "E10 explicit check ignores mac":
        ("{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys", "{\"entity\", \"crf_in\", \"crf_out\"} <= keys"),
    "E11 explicit check ignores crf":
        ("{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys", "{\"entity\", \"mac\"} <= keys"),
    "E12 explicit check ignores listener shape":
        ("                or not {\"listeners\", \"listener_index_set\"} & keys):",
         "                or False):"),
    "E13 explicit check ignores talker shape":
        ("                or not {\"talkers\", \"talker_index_set\"} & keys", "                or False"),
    "E14 CLI always explicit":
        ("topology_explicit=_release_topology_explicit(a.dut, a.peer))", "topology_explicit=True)"),
    "E15 empty values count as explicit":
        ("                if \"=\" in part and part.split(\"=\", 1)[1].strip()}",
         "                if \"=\" in part}"),
    "E16 topology_explicit type not validated":
        ("        if type(self.topology_explicit) is not bool:", "        if False:"),
    "E17 default attests explicit":
        ("    topology_explicit: bool = False", "    topology_explicit: bool = True"),
    # ---- CRF overlap (R347 S2 as recorded in the decision)
    "O01 overlap refusal removed":
        ("            raise ValueError(\"release AAF indices must not include a CRF index\")",
         "            pass"),
    "O02 overlap checks talker side only":
        ("        if (device.crf_out in device.talker_indices(False)\n                or device.crf_in in device.listener_indices(False)):",
         "        if (device.crf_out in device.talker_indices(False)):"),
    "O03 overlap checks listener side only":
        ("        if (device.crf_out in device.talker_indices(False)\n                or device.crf_in in device.listener_indices(False)):",
         "        if (device.crf_in in device.listener_indices(False)):"),
    "O04 overlap checks DUT only":
        ("    for device in (dut, peer):\n        if (device.crf_out", "    for device in (dut,):\n        if (device.crf_out"),
    # ---- #366 boot oracle
    "B01 boot oracle ignores restarts":
        ("\"PASS\" if boot_passes == 1 and restarts == 0 else", "\"PASS\" if boot_passes == 1 else"),
    "B02 boot oracle accepts two passes":
        ("\"PASS\" if boot_passes == 1 and restarts == 0 else", "\"PASS\" if boot_passes >= 1 and restarts == 0 else"),
    "B03 boot oracle ignores capture completeness":
        ("    if (capture_complete is not True or type(boot_passes) is not int",
         "    if (type(boot_passes) is not int"),
    "B04 boot oracle accepts bool":
        ("or type(restarts) is not int or boot_passes < 0 or restarts < 0):",
         "or not isinstance(restarts, int) or boot_passes < 0 or restarts < 0):"),
    "B05 single-boot assertion dropped":
        ("    AssertSpec(\"power.single-boot\", RELEASE_CLAUSE +",
         "    ) and None or (AssertSpec(\"power.single-boot\", RELEASE_CLAUSE +"),
    "B06 boot max passes 2":
        ("boot_max_passes=1, boot_max_restarts=0,", "boot_max_passes=2, boot_max_restarts=0,"),
    "B07 boot max restarts 1":
        ("boot_max_passes=1, boot_max_restarts=0,", "boot_max_passes=1, boot_max_restarts=1,"),
    "B08 boot oracle accepts zero passes":
        ("\"PASS\" if boot_passes == 1 and restarts == 0 else", "\"PASS\" if boot_passes <= 1 and restarts == 0 else"),
    "B09 boot oracle accepts negative restarts":
        ("or type(restarts) is not int or boot_passes < 0 or restarts < 0):",
         "or type(restarts) is not int or boot_passes < 0):"),
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
