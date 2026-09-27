#!/usr/bin/env python3
"""R363-2 reviewer mutants, independent of the executor's driver.

Usage: reviewer_mutants.py <clone> <scratch-dir> <probe.py>
Each mutant edits a scratch copy of tb/tools/torture_campaign.py only (unique anchor
required), then runs the unchanged planner self-test. KILLED means the self-test
returned non-zero; SURVIVED means it stayed green. The reviewer probe verdict on the
same mutant is recorded as a second, independent signal. At most 8 parallel jobs.
"""
from __future__ import annotations

import concurrent.futures
import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = (
    ("M01 history coverage drops the R allowance for interval grading",
     "        covered_gm_s = [event for event in gm_changes_s\n                        if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "        covered_gm_s = [event for event in gm_changes_s\n                        if start_s <= Decimal(str(event)) < clear_s]"),
    ("M02 history final coverage includes the clear instant",
     "        if not any(start_s - resolution_s <= gm_s < clear_s",
     "        if not any(start_s - resolution_s <= gm_s <= clear_s"),
    ("M03 history final coverage widened to 2R",
     "        if not any(start_s - resolution_s <= gm_s < clear_s",
     "        if not any(start_s - 2 * resolution_s <= gm_s < clear_s"),
    ("M04 history allows touching intervals",
     "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):",
     "if clear_s <= start_s or (intervals and start_s < intervals[-1][1]):"),
    ("M05 history grades interval against every GM change",
     "            gm_changes_s=covered_gm_s)",
     "            gm_changes_s=gm_changes_s)"),
    ("M06 history grades no GM minimum inside intervals",
     "            gm_changes_s=covered_gm_s)",
     "            gm_changes_s=[])"),
    ("M07 history resolution ceiling raised to 0.5",
     "or not 0 <= observation_resolution_s < 0.25):",
     "or not 0 <= observation_resolution_s < 0.5):"),
    ("M08 rise check drops the R allowance",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if min(events_s) > observed_start_s:"),
    ("M09 rise check widened to 2R",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if min(events_s) > observed_start_s + 2 * observation_resolution_s:"),
    ("M10 rise check uses the last event",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if max(events_s) > observed_start_s + observation_resolution_s:"),
    ("M11 tu resolution limit uses the 0.5 s bound only",
     "resolution_limit_s = min(0.25, holdover_bound_s)",
     "resolution_limit_s = holdover_bound_s"),
    ("M12 tu resolution limit equality accepted",
     "    if observation_resolution_s >= resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the tu timing limits\")",
     "    if observation_resolution_s > resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the tu timing limits\")"),
    ("M13 mr resolution limit is the full second",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2\n    detail[",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S\n    detail["),
    ("M14 mr resolution limit equality accepted",
     "    if observation_resolution_s >= resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the mr cause window\")",
     "    if observation_resolution_s > resolution_limit_s:\n        return \"NOT RUN\", dict(detail, why=\"resolution cannot decide the mr cause window\")"),
    ("M15 mr consumes the latest eligible cause",
     "        causes.remove(matches[0])",
     "        causes.remove(matches[-1])"),
    ("M16 mr causes sorted latest first",
     'causes = sorted(causes, key=lambda event: event["timestamp_s"])',
     'causes = sorted(causes, key=lambda event: -event["timestamp_s"])'),
    ("M17 mr PHC step accepted as a cause (#602 ruling reversed)",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle", "PHC settime/adjtime"}'),
    ("M18 capture start requirement drops R",
     "                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))\n                        - Decimal(str(observation_resolution_s)))\n    detail.update(capture_window_s",
     "                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S)))\n    detail.update(capture_window_s"),
    ("M19 capture start requirement drops the 1 s update ceiling",
     "    required_start_s = (Decimal(str(reads[0][\"timestamp_s\"]))\n                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))\n",
     "    required_start_s = (Decimal(str(reads[0][\"timestamp_s\"]))\n"),
    ("M20 capture start anchored at the last read",
     'required_start_s = (Decimal(str(reads[0]["timestamp_s"]))',
     'required_start_s = (Decimal(str(reads[-1]["timestamp_s"]))'),
    ("M21 capture PDU containment excludes the window end",
     'or any(not capture_start_s <= Decimal(str(pdu["timestamp_s"])) <= capture_end_s',
     'or any(not capture_start_s <= Decimal(str(pdu["timestamp_s"])) < capture_end_s'),
    ("M22 boolean capture silently accepted without PDUs",
     "    if capture_window_s is None and stream_pdus:\n",
     "    if capture_window_s is None and not stream_pdus:\n        capture_window_s = (-1e9, 1e9)\n    if capture_window_s is None and stream_pdus:\n"),
    ("M23 counter decrease decoded as a wrap again",
     '        if after["value"] < before["value"]:\n            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",\n                            "before": before["value"], "after": after["value"]}\n        delta = after["value"] - before["value"]',
     '        delta = (after["value"] - before["value"]) % 2**32'),
    ("M24 counter decrease reported NOT RUN",
     '            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",',
     '            return "NOT RUN", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",'),
    ("M25 ReleaseCapture defaults to incomplete",
     "    window_s: tuple[float, float]\n    complete: bool = True",
     "    window_s: tuple[float, float]\n    complete: bool = False"),
    ("M26 single-interval entry drops GM changes before the rise",
     "    gm_events_s = gm_changes_s\n",
     "    gm_events_s = [event_s for event_s in gm_changes_s if event_s >= start_s]\n"),
    ("M27 history uncovered GM reported NOT RUN",
     'return "FAIL", dict(detail, why="GM change lacks a covering tu minimum", gm_change_s=event)',
     'return "NOT RUN", dict(detail, why="GM change lacks a covering tu minimum", gm_change_s=event)'),
    ("M28 history empty-interval coarse-resolution guard removed",
     "            or not 0 <= observation_resolution_s < 0.25):",
     "            or not 0 <= observation_resolution_s):"),
)


def run(clone: Path, scratch: Path, probe: Path, index: int, name: str, old: str, new: str) -> str:
    source = (clone / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
    if source.count(old) != 1:
        return f"ANCHOR-ERROR {name}: count={source.count(old)}"
    work = scratch / f"m{index:02d}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    target = work / "torture_campaign.py"
    target.write_text(source.replace(old, new), encoding="utf-8")
    st = subprocess.run([sys.executable, "-B", str(target), "--self-test"], capture_output=True,
                        text=True, timeout=900)
    failed = sorted({line.split()[1] for line in st.stderr.splitlines()
                     if line.startswith(("FAIL: ", "ERROR: "))})
    pr = subprocess.run([sys.executable, "-B", str(probe), str(target)], capture_output=True,
                        text=True, timeout=900)
    unmet = [line.split(":")[0][6:] for line in pr.stdout.splitlines() if line.startswith("UNMET")]
    verdict = "KILLED" if st.returncode != 0 else "SURVIVED"
    return (f"{verdict} {name}: self-test rc={st.returncode} failing={failed or '-'}; "
            f"probe rc={pr.returncode} unmet={unmet or '-'}")


def main() -> int:
    clone, scratch, probe = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(run, clone, scratch, probe, i, *m) for i, m in enumerate(MUTANTS, 1)]
        lines = [f.result() for f in futures]
    for line in lines:
        print(line)
    killed = sum(line.startswith("KILLED") for line in lines)
    print(f"reviewer mutants: {killed}/{len(lines)} killed by the planner self-test")
    return 0 if all(not line.startswith("ANCHOR") for line in lines) else 2


if __name__ == "__main__":
    raise SystemExit(main())
