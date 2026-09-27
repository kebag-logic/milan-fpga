#!/usr/bin/env python3
"""R346-3 probe (round-3 delta 24d32d54..8153576a): source mutants of the release planner and
its plan steps, each graded by the head's own gates (planner --self-test and the plan feature
under behave).

Usage: python3 -B planner_mutants_r3.py <repo-root> <scratch-dir>
A pristine copy of tb/tools, tests and scripts is exported from HEAD with `git archive` into
<scratch-dir>/base; each mutant runs in its own copy.  Killed = at least one gate exits
non-zero.  INVALID = the anchor does not match exactly once (never counted as a kill).
Entries tagged [info] probe prose/assertion-text pinning or test-oracle redundancy and are
reported, not required; [equiv] marks a behaviorally equivalent mutant (not required).
The repository is never written.
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
STEPS = "tests/steps/torture_release_steps.py"

# name: (file, old, new)
M = {
    # ---- restoration eligibility ceiling (decision 5855515133 item 1)
    "N01 restore eligibility check dropped":
        (PLANNER, "            and settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S\n", ""),
    "N02 restore ceiling exclusive (<)":
        (PLANNER, "settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S",
         "settings.restore_bound_s < RELEASE_RESTORE_BOUND_S"),
    "N03 restore ceiling 31":
        (PLANNER, "RELEASE_RESTORE_BOUND_S = 30\n", "RELEASE_RESTORE_BOUND_S = 31\n"),
    "N04 restore ceiling 60":
        (PLANNER, "RELEASE_RESTORE_BOUND_S = 30\n", "RELEASE_RESTORE_BOUND_S = 60\n"),
    "N05 power area skips shared profile check":
        (PLANNER, "        args[\"release_eligible\"] &= _release_profile_eligible(settings)\n"
                  "        args[\"topology_explicit\"] = settings.topology_explicit\n",
         "        args[\"topology_explicit\"] = settings.topology_explicit\n"),
    "N06 soak area skips shared profile check":
        (PLANNER, "    args[\"release_eligible\"] &= _release_profile_eligible(settings)\n    args[\"max_soak_interval_s\"]",
         "    args[\"max_soak_interval_s\"]"),
    # ---- ADP window (decision item 3); R13/R19 of round 2 retargeted to the new anchors
    "N07 (R13') ADP deadline literal 20":
        (PLANNER, "adp_deadline=\"2 * pre_cut_valid_time\",", "adp_deadline=\"20\","),
    "N08 ADP deadline charges the hold":
        (PLANNER, "adp_deadline=\"2 * pre_cut_valid_time\",",
         "adp_deadline=\"2 * pre_cut_valid_time - power_off_hold_s\","),
    "N09 ADP start at pre-cut advert":
        (PLANNER, "adp_start=\"T0\",", "adp_start=\"last pre-cut ENTITY_AVAILABLE\","),
    "N10 ADP required valid_time 31":
        (PLANNER, "adp_required_valid_time=10,", "adp_required_valid_time=31,"),
    "N11 ADP required valid_time key dropped":
        (PLANNER, "                    adp_required_valid_time=10,\n", ""),
    "N12 (R19') ADP missing/expired weakened":
        (PLANNER, "adp_missing_or_expired=\"fail; require captured valid_time=10 and arrival before T0 deadline\",",
         "adp_missing_or_expired=\"fail\","),
    "N13 ADP elapsed from power OFF":
        (PLANNER, "adp_elapsed=\"first_post_cut_available_host_s - t0_host_s\",",
         "adp_elapsed=\"first_post_cut_available_host_s - power_off_host_s\","),
    "N14 hold charged to ADP window flag":
        (PLANNER, "power_off_hold_in_adp_window=False,", "power_off_hold_in_adp_window=True,"),
    # ---- power-off hold as a recorded parameter
    "N15 hold not validated":
        (PLANNER, "\"power_cycles\", \"power_off_hold_s\",", "\"power_cycles\","),
    "N16 hold default 5":
        (PLANNER, "    power_off_hold_s: int = 8\n", "    power_off_hold_s: int = 5\n"),
    "N17 hold origin dropped":
        (PLANNER, "                    power_off_hold_origin=\"phys.dut-cycle.power-cycle: default 8 s; verify discharge\",\n", ""),
    "N18 [equiv] CLI hold default hardcoded 8":
        (PLANNER, "default=ReleaseSettings.power_off_hold_s,", "default=8,"),
    # ---- tu contract (decision item 2)
    "N19 tu bound 0.25 (B.1.1 only)":
        (PLANNER, "tu_holdover_bound_s=0.5,", "tu_holdover_bound_s=0.25,"),
    "N20 tu origin any time":
        (PLANNER, "tu_time_origin=\"recorded GM change or timing discontinuity\",",
         "tu_time_origin=\"first observed tu\","),
    "N21 tu resolution unrecorded":
        (PLANNER, "tu_observation_resolution=\"record measured resolution in seconds with event evidence\",",
         "tu_observation_resolution=\"not recorded\","),
    "N22 tu evidence dropped from continuous list":
        (PLANNER, "continuous_evidence=[\"asCapable_transitions\", \"tu_intervals\",",
         "continuous_evidence=[\"asCapable_transitions\","),
    "N23 [info] tu assertion text reverted to round 2":
        (PLANNER, "\"each tu interval begins with a recorded GM change or timing \"",
         "\"correlate timestamped discontinuities and wire tu with the \""),
    "N24 [info] ADP assertion text charges pre-cut expiry":
        (PLANNER, "\"first post-cut ENTITY_AVAILABLE arrives within the advertised \"",
         "\"first post-cut ENTITY_AVAILABLE arrives before the pre-cut expiry \""),
    # ---- topology explicitness (decision item 4)
    "N25 explicit check ignores entity":
        (PLANNER, "{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys", "{\"mac\", \"crf_in\", \"crf_out\"} <= keys"),
    "N26 explicit check ignores crf_in only":
        (PLANNER, "{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys", "{\"entity\", \"mac\", \"crf_out\"} <= keys"),
    "N27 explicit check ignores crf_out only":
        (PLANNER, "{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys", "{\"entity\", \"mac\", \"crf_in\"} <= keys"),
    "N28 explicit check peer only":
        (PLANNER, "    for spec in (dut_spec, peer_spec):\n        keys =", "    for spec in (peer_spec,):\n        keys ="),
    "N29 explicit check dut only":
        (PLANNER, "    for spec in (dut_spec, peer_spec):\n        keys =", "    for spec in (dut_spec,):\n        keys ="),
    "N30 listener_index_set not accepted":
        (PLANNER, "{\"listeners\", \"listener_index_set\"} & keys", "{\"listeners\"} & keys"),
    "N31 entity_id alias accepted":
        (PLANNER, "{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys",
         "{\"mac\", \"crf_in\", \"crf_out\"} <= keys and bool({\"entity\", \"entity_id\"} & keys)"),
    # ---- boot evidence window
    "N32 boot evidence stops at minimum window":
        (PLANNER, "boot_evidence=\"complete UART/reset observation from T0 through next cut or campaign end; \"",
         "boot_evidence=\"complete UART/reset observation from T0 through boot_observation_s; \""),
    "N33 boot oracle accepts bool restarts":
        (PLANNER, "or type(restarts) is not int or boot_passes < 0 or restarts < 0):",
         "or not isinstance(restarts, int) or boot_passes < 0 or restarts < 0):"),
    # ---- step-file weakening: does the feature still fail if its own oracle weakens?
    "S01 [info] step drops redundant eligible oracle":
        (STEPS, "        assert step[\"args\"][\"release_eligible\"] is False\n", ""),
}


def run(name: str, fname: str, old: str, new: str) -> tuple[str, str, str]:
    work = scratch / ("m_" + name.split()[0])
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(base, work, symlinks=True)
    path = work / fname
    text = path.read_text()
    if text.count(old) != 1:
        shutil.rmtree(work)
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
pristine = subprocess.run([sys.executable, "-B", PLANNER, "--self-test"], cwd=base,
                          capture_output=True, text=True).returncode
pristine_b = subprocess.run([sys.executable, "-B", "-m", "behave",
                             "tests/features/torture_campaign_plan.feature", "-f", "plain"],
                            cwd=base, capture_output=True, text=True).returncode
print(f"pristine: self-test rc={pristine} behave rc={pristine_b}")
if pristine or pristine_b:
    sys.exit(1)
with cf.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(lambda kv: run(kv[0], *kv[1]), M.items()))
for name, verdict, how in results:
    print(f"{verdict:9s} {name:55s} {how}")
required = [r for r in results if "[info]" not in r[0] and "[equiv]" not in r[0]]
print(f"{len(results)} mutants ({len(required)} required): "
      f"{sum(r[1] == 'KILLED' for r in results)} killed, "
      f"{sum(r[1] == 'SURVIVED' for r in results)} survived, "
      f"{sum(r[1] == 'INVALID' for r in results)} invalid; "
      f"required not killed: {[r[0] for r in required if r[1] != 'KILLED']}")
sys.exit(0)
