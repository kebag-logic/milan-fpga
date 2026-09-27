#!/usr/bin/env python3
"""Reviewer mutants for the round-3 tu/mr changes; run the unchanged planner self-test.

usage: r3_mutants.py <planner.py>
A mutant is KILLED when the self-test exits nonzero with a named FAIL (not only ERROR),
CRASH-ONLY when it fails only by ERROR, and SURVIVED when the self-test still passes.
Only a temporary copy changes.
"""
import re, subprocess, sys, tempfile
from pathlib import Path

M = [
 ("R3-01 minimum ignores R", "clear_s + observation_resolution_s < minimum_clear_s", "clear_s < minimum_clear_s"),
 ("R3-02 minimum uses 2R", "clear_s + observation_resolution_s < minimum_clear_s", "clear_s + 2 * observation_resolution_s < minimum_clear_s"),
 ("R3-03 minimum uses R/2", "clear_s + observation_resolution_s < minimum_clear_s", "clear_s + observation_resolution_s / 2 < minimum_clear_s"),
 ("R3-04 minimum admits equality-fail", "clear_s + observation_resolution_s < minimum_clear_s", "clear_s + observation_resolution_s <= minimum_clear_s"),
 ("R3-05 limit slightly smaller", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.1249995"),
 ("R3-06 limit slightly larger", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.1250005"),
 ("R3-07 limit 0.2", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.25 / 2", "RELEASE_TU_RESOLUTION_LIMIT_S = 0.2"),
 ("R3-08 single limit check removed", "    if observation_resolution_s >= resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the tu timing limits\")\n", ""),
 ("R3-09 single local limit one-sided", "    resolution_limit_s = RELEASE_TU_RESOLUTION_LIMIT_S\n    detail = {\"observation_resolution_s\": observation_resolution_s,\n              \"resolution_limit_s\": resolution_limit_s}",
                                         "    resolution_limit_s = 0.25\n    detail = {\"observation_resolution_s\": observation_resolution_s,\n              \"resolution_limit_s\": RELEASE_TU_RESOLUTION_LIMIT_S}"),
 ("R3-10 history limit one-sided", "or not 0 <= observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S):", "or not 0 <= observation_resolution_s < 0.25):"),
 ("R3-11 deadline drops R", "deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s", "deadline_s = last_discontinuity_s + holdover_bound_s"),
 ("R3-12 latest clear 2R", "latest_clear_s = clear_s + observation_resolution_s", "latest_clear_s = clear_s + 2 * observation_resolution_s"),
 ("R3-13 upper uses clear minus R", "latest_clear_s = clear_s + observation_resolution_s", "latest_clear_s = clear_s - observation_resolution_s"),
 ("R3-14 deadline adds 2R", "deadline_s = last_discontinuity_s + holdover_bound_s + observation_resolution_s", "deadline_s = last_discontinuity_s + holdover_bound_s + 2 * observation_resolution_s"),
 ("R3-15 history loop2 drops start allowance", "        if not any(start_s - resolution_s <= gm_s < clear_s", "        if not any(start_s <= gm_s < clear_s"),
 ("R3-16 history loop2 strict start", "        if not any(start_s - resolution_s <= gm_s < clear_s", "        if not any(start_s - resolution_s < gm_s < clear_s"),
 ("R3-17 history loop2 includes clear", "        if not any(start_s - resolution_s <= gm_s < clear_s", "        if not any(start_s - resolution_s <= gm_s <= clear_s"),
 ("R3-18 history loop2 removed", "            return \"FAIL\", dict(detail, why=\"GM change lacks a covering tu minimum\", gm_change_s=event)", "            pass"),
 ("R3-19 history grades all GMs per interval", "            gm_changes_s=covered_gm_s)", "            gm_changes_s=gm_changes_s)"),
 ("R3-20 history separation removed", "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):", "if clear_s <= start_s:"),
 ("R3-21 history positive duration removed", "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):", "if (intervals and start_s <= intervals[-1][1]):"),
 ("R3-22 history holdover changed", "    holdover_bound_s = 0.5\n    detail = {\"observation_resolution_s\": observation_resolution_s,\n              \"resolution_limit_s\": RELEASE_TU_RESOLUTION_LIMIT_S}", "    holdover_bound_s = 0.6\n    detail = {\"observation_resolution_s\": observation_resolution_s,\n              \"resolution_limit_s\": RELEASE_TU_RESOLUTION_LIMIT_S}"),
 ("R3-23 latest_clear detail dropped", "clear_s=float(clear_s), latest_clear_s=float(latest_clear_s),", "clear_s=float(clear_s),"),
 ("R3-24 latest_clear detail wrong", "clear_s=float(clear_s), latest_clear_s=float(latest_clear_s),", "clear_s=float(clear_s), latest_clear_s=float(clear_s),"),
 ("R3-25 deadline detail wrong", "deadline_s=float(deadline_s),\n", "deadline_s=float(deadline_s - observation_resolution_s),\n"),
 ("R3-26 mr limit doubled", "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2\n    detail = {", "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S\n    detail = {"),
 ("R3-27 mr limit equality admitted", "    if observation_resolution_s >= resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the mr cause window\")", "    if observation_resolution_s > resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the mr cause window\")"),
 ("R3-28 plan tu limit 0.25", "tu_resolution_limit_s=RELEASE_TU_RESOLUTION_LIMIT_S,", "tu_resolution_limit_s=0.25,"),
 ("R3-29 text limit 0.25", "\"resolution_limit_s is 0.125 s; \"", "\"resolution_limit_s is 0.25 s; \""),
 ("R3-30 text minimum sign", "\"minimum accepts h + R >= 0.25 s, so d >= 0.25 s - 2 * R; \"", "\"minimum accepts h - R >= 0.25 s, so d >= 0.25 s; \""),
 ("R3-31 text upper", "\"upper bound requires h + R <= 0.5 s + R, equivalently h <= 0.5 s; \"", "\"upper bound requires h <= 0.5 s + R; \""),
 ("R3-32 mr cause_window detail key dropped", "              \"cause_window\": \"toggle timestamp +/- observation_resolution_s\",\n", ""),
 ("R3-33 mr empty stream id accepted", "or not record[\"stream_id\"] or not _release_finite", "or not _release_finite"),
 ("R3-34 mr negative pdu index", " or pdu[\"pdu_index\"] < 0\n", "\n"),
 ("R3-35 single uncorrelated detail dropped", "return \"FAIL\", {\"why\": \"uncorrelated tu fails\", **detail}", "return \"FAIL\", {\"why\": \"uncorrelated tu fails\"}"),
 ("R3-36 history NOT RUN drops limit on sub-verdict", "            return verdict, dict(detail, interval=interval, evidence=evidence)", "            return verdict, dict(interval=interval, evidence=evidence)"),
 ("R3-37 media reset NOT RUN drops detail", "    verdict, evidence = _release_mr_toggles(stream_pdus, stream_causes, observation_resolution_s)\n    detail.update(evidence)\n    if verdict != \"PASS\":\n        return verdict, detail", "    verdict, evidence = _release_mr_toggles(stream_pdus, stream_causes, observation_resolution_s)\n    detail.update(evidence)\n    if verdict != \"PASS\":\n        return verdict, evidence"),
 ("R3-38 minimum uses first GM", "minimum_clear_s = max(gm_events_s) + Decimal(\"0.25\") if gm_events_s else None", "minimum_clear_s = min(gm_events_s) + Decimal(\"0.25\") if gm_events_s else None"),
 ("R3-39 minimum 0.2", "minimum_clear_s = max(gm_events_s) + Decimal(\"0.25\") if gm_events_s else None", "minimum_clear_s = max(gm_events_s) + Decimal(\"0.2\") if gm_events_s else None"),
]

def main():
    src = Path(sys.argv[1]); text = src.read_text(encoding="utf-8")
    bad = 0
    with tempfile.TemporaryDirectory() as d:
        cand = Path(d) / "torture_campaign.py"
        cand.write_text(text, encoding="utf-8")
        base = subprocess.run([sys.executable, "-B", str(cand), "--self-test"], capture_output=True, text=True, timeout=600)
        print("BASELINE", "OK" if base.returncode == 0 and "\nOK\n" in base.stderr else "BROKEN")
        for name, old, new in M:
            n = text.count(old)
            if n != 1:
                print(f"ANCHOR({n}): {name}"); bad += 1; continue
            cand.write_text(text.replace(old, new), encoding="utf-8")
            r = subprocess.run([sys.executable, "-B", str(cand), "--self-test"], capture_output=True, text=True, timeout=600)
            fails = sorted(set(re.findall(r"^FAIL: (\w+)", r.stderr, re.M)))
            errs = sorted(set(re.findall(r"^ERROR: (\w+)", r.stderr, re.M)))
            if r.returncode == 0:
                state = "SURVIVED"; bad += 1
            elif fails:
                state = "KILLED"
            else:
                state = "CRASH-ONLY"
            print(f"{state}: {name}: FAIL={fails} ERROR={errs}")
    print(f"mutants: {len(M)}; survived/anchor problems: {bad}")

if __name__ == "__main__":
    main()
