#!/usr/bin/env python3
"""[R362] round-2 independent mutation probe for PR #601 (issue #593).

Usage: python3 -B r362_2_mutants.py <repo-checkout> <scratch-dir>

Copies tb/ and tests/ from the checkout into <scratch-dir>/tree, applies one
source mutation at a time to the COPY of tb/tools/torture_campaign.py, and runs
(1) the planner self-test and, if that passes, (2) the plan feature under
behave, both from the copy. The checkout is never written. A mutant is KILLED
only if a run exits non-zero with a failing test/scenario; an anchor that is
not unique is reported as ANCHOR-ERROR (no verdict).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PLANNER = "tb/tools/torture_campaign.py"

TU_LIMIT = ('    if observation_resolution_s >= resolution_limit_s:\n'
            '        return "NOT RUN", dict(detail, why="resolution cannot decide the tu timing limits")')
MR_LIMIT = ('    if observation_resolution_s >= resolution_limit_s:\n'
            '        return "NOT RUN", dict(detail, why="resolution cannot decide the mr cause window")')

# (id, description, old, new) -- old must occur exactly once.
MUTANTS = [
    # --- item 1: rise correlation -------------------------------------------------
    ("C01", "rise allowance doubled",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if min(events_s) > observed_start_s + 2 * observation_resolution_s:"),
    ("C02", "rise allowance dropped (stricter)",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if min(events_s) > observed_start_s:"),
    ("C03", "rise judged on the last event",
     "if min(events_s) > observed_start_s + observation_resolution_s:",
     "if max(events_s) > observed_start_s + observation_resolution_s + 10:"),
    # --- item 2: GM coverage / minimum ---------------------------------------------
    ("C04", "coverage loop drops start allowance",
     "        if not any(start_s - resolution_s <= gm_s < clear_s\n",
     "        if not any(start_s <= gm_s < clear_s\n"),
    ("C05", "coverage loop includes clear instant",
     "        if not any(start_s - resolution_s <= gm_s < clear_s\n",
     "        if not any(start_s - resolution_s <= gm_s <= clear_s\n"),
    ("C06", "covered GM window drops start allowance",
     "if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "if start_s <= Decimal(str(event)) < clear_s]"),
    ("C07", "covered GM window includes clear instant",
     "if start_s - resolution_s <= Decimal(str(event)) < clear_s]",
     "if start_s - resolution_s <= Decimal(str(event)) <= clear_s]"),
    ("C08", "history passes all GM changes to every interval",
     "            gm_changes_s=covered_gm_s)",
     "            gm_changes_s=gm_changes_s)"),
    ("C09", "history allows touching intervals",
     "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):",
     "if clear_s <= start_s or (intervals and start_s < intervals[-1][1]):"),
    ("C10", "history accepts negative resolution",
     "or not 0 <= observation_resolution_s < 0.25):",
     "or not observation_resolution_s < 0.25):"),
    ("C11", "single-interval minimum uses first covered GM",
     "gm_events_s = gm_changes_s\n",
     "gm_events_s = sorted(gm_changes_s)[:1]\n"),
    ("C12", "single-interval minimum 0.25 -> 0.2",
     'max(gm_events_s) + Decimal("0.25")', 'max(gm_events_s) + Decimal("0.2")'),
    # --- item 3: deciding resolution ------------------------------------------------
    ("C13", "tu limit admits equality", TU_LIMIT,
     TU_LIMIT.replace(">= resolution_limit_s", "> resolution_limit_s")),
    ("C14", "mr limit admits equality", MR_LIMIT,
     MR_LIMIT.replace(">= resolution_limit_s", "> resolution_limit_s")),
    ("C15", "tu limit derived from 0.5 s only",
     "    resolution_limit_s = min(0.25, holdover_bound_s)\n",
     "    resolution_limit_s = holdover_bound_s\n"),
    ("C16", "mr limit is the full 1 s ceiling",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2\n",
     "    resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S\n"),
    ("C17", "tu verdict omits stated limit",
     '    detail["resolution_limit_s"] = resolution_limit_s\n' + TU_LIMIT,
     TU_LIMIT),
    ("C18", "mr verdict omits stated limit",
     '    detail["resolution_limit_s"] = resolution_limit_s\n' + MR_LIMIT,
     MR_LIMIT),
    ("C19", "history verdict omits stated limit",
     '              "resolution_limit_s": min(0.25, holdover_bound_s)}',
     '              }'),
    ("C20", "history limit admits equality",
     "or not 0 <= observation_resolution_s < 0.25):",
     "or not 0 <= observation_resolution_s <= 0.25):"),
    ("C21", "history limit relaxed to 0.5",
     "or not 0 <= observation_resolution_s < 0.25):",
     "or not 0 <= observation_resolution_s < 0.5):"),
    # --- item 4: distinct causes ---------------------------------------------------
    ("C22", "latest eligible cause consumed",
     "        causes.remove(matches[0])", "        causes.remove(matches[-1])"),
    # --- item 7: capture span / reset ------------------------------------------------
    ("C23", "capture start drops 1 s term",
     '    required_start_s = (Decimal(str(reads[0]["timestamp_s"]))\n'
     '                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))\n',
     '    required_start_s = (Decimal(str(reads[0]["timestamp_s"]))\n'),
    ("C24", "capture start drops R term",
     '                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S))\n'
     '                        - Decimal(str(observation_resolution_s)))\n',
     '                        - Decimal(str(MILAN_MAX_OBSERVATION_INTERVAL_S)))\n'),
    ("C25", "capture end judged at first read",
     'or capture_end_s < Decimal(str(reads[-1]["timestamp_s"]))',
     'or capture_end_s < Decimal(str(reads[0]["timestamp_s"]))'),
    ("C26", "PDU-endpoint fallback removed",
     "    if capture_window_s is None and stream_pdus:\n",
     "    if False:\n"),
    ("C27", "decrease treated as no change",
     '    if after["value"] < before["value"]:\n'
     '            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",',
     '    if after["value"] < before["value"]:\n'
     '            continue\n'
     '            return "FAIL", {"why": "MEDIA_RESET decreased: counter reset; check talker start evidence",'),
    ("C28", "decrease decoded as 32-bit wrap",
     '        if after["value"] < before["value"]:\n',
     '        if after["value"] < before["value"] and False:\n'),
    ("C29", "MEDIA_RESET lower edge drops R",
     '                   - Decimal(str(resolution_s)))\n        upper_s',
     ')\n        upper_s'),
    # --- carried checks (round 1) at boundaries -------------------------------------
    ("C30", "eight-PDU hold -> seven",
     'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 7:'),
    ("C31", "eight-PDU hold -> nine",
     'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 9:'),
    ("C32", "terminal hold -> seven",
     'if toggles and pdus[-1]["pdu_index"] - toggles[-1]["pdu_index"] + 1 < 8:',
     'if toggles and pdus[-1]["pdu_index"] - toggles[-1]["pdu_index"] + 1 < 7:'),
    ("C33", "PDU contiguity ignored",
     'if (current["pdu_index"] != previous["pdu_index"] + 1\n',
     'if (False\n'),
    ("C34", "empty stream id accepted",
     '        if (not isinstance(record, dict) or not isinstance(record.get("stream_id"), str)\n'
     '                or not record["stream_id"] or',
     '        if (not isinstance(record, dict) or not isinstance(record.get("stream_id"), str)\n'
     '                or'),
    ("C35", "negative pdu index accepted",
     ' or pdu["pdu_index"] < 0\n', '\n'),
    ("C36", "mr bit range ignored",
     ' or pdu["mr"] not in (0, 1)):', '):'),
    ("C37", "tu negative resolution accepted",
     "holdover_bound_s != 0.5 or observation_resolution_s < 0:",
     "holdover_bound_s != 0.5:"),
    ("C38", "cause window text in verdict changed",
     '"cause_window": "toggle timestamp +/- observation_resolution_s",',
     '"cause_window": "fixed",'),
    ("C39", "plan cause window arg weakened",
     'mr_cause_window="toggle timestamp +/- observation_resolution_s",',
     'mr_cause_window="fixed 10 ms",'),
    ("C40", "plan tu_gm_minimum_check weakened",
     'tu_gm_minimum_check="clear + observation_resolution_s >= GM change + 0.25 s",',
     'tu_gm_minimum_check="optional",'),
    ("C41", "plan evidence list drops gm_changes",
     '"MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes"],',
     '"MEDIA_RESET_reads", "gptp_discontinuities"],'),
    ("C42", "plan tu kinds drop GM time-source change",
     '"GM time-source change", "other detected gPTP discontinuity"],',
     '"other detected gPTP discontinuity"],'),
    ("C43", "exit code ignores NOT RUN",
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN", "NOT RUN") for r in records)',
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN") for r in records)'),
]

# Assertion-text deletions: every string-literal line this PR added to the two
# new/changed soak assertions, deleted one at a time.
MR_TEXT = [
    '"; IEEE 1722-2016 4.4.4.3; Milan v1.2 Annex B.1.2, Tables 5.4/5.6: "',
    '"every mr toggle and MEDIA_RESET increment needs a recorded "',
    '"media-clock-source change, CRF disruption, or received CRF mr toggle "',
    '"mapped to that stream\'s clock source; GM change alone fails; "',
    '"match causes within +/- observation_resolution_s of the toggle; "',
    '"hold each new value for at least 8 AVTPDUs of that stream; "',
    '"MEDIA_RESET counts observation intervals, not packets; "',
    '"missing packet, cause, counter or resolution evidence is NOT RUN; "',
    '"each cause excuses at most one toggle per stream; "',
    '"2 * observation_resolution_s must be less than the 1 s counter interval ceiling; "',
    '"capture must span [first read - 1 s - observation_resolution_s, last read]; "',
]
TU_TEXT = [
    '"GM-identity edge, GM time-source change, or other detected gPTP discontinuity "',
    '"(including PHC settime/adjtime and fabric discontinuity); "',
    '"after each GM change, clear + observation_resolution_s must be at least "',
    '"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "',
    '"first discontinuity must be within observation_resolution_s of the rise; "',
    '"grade every GM change against the complete tu interval history; "',
    '"a GM change with no covering interval fails; "',
    '"observation_resolution_s must be less than min(0.25 s, 0.5 s); "',
]
for i, lit in enumerate(MR_TEXT + TU_TEXT):
    MUTANTS.append((f"T{i + 1:02d}", "assertion text deleted: " + lit, lit, '""'))
# Sub-phrase weakenings of key tokens (a deleted word, not a whole line).
MUTANTS += [
    ("T20", "mr text: 8 -> 7 AVTPDUs", "at least 8 AVTPDUs of that stream", "at least 7 AVTPDUs of that stream"),
    ("T21", "mr text: +/- window made one-sided",
     "match causes within +/- observation_resolution_s of the toggle",
     "match causes within observation_resolution_s after the toggle"),
    ("T22", "tu text: 0.25 s -> 0.2 s", "GM change + 0.25 s (Annex B.1.1 minimum)",
     "GM change + 0.2 s (Annex B.1.1 minimum)"),
    ("T23", "tu text: min(0.25 s, 0.5 s) -> 0.5 s",
     "observation_resolution_s must be less than min(0.25 s, 0.5 s)",
     "observation_resolution_s must be less than 0.5 s"),
    ("T24", "mr text: GM change alone fails -> passes", "GM change alone fails", "GM change alone passes"),
]


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)


def main() -> int:
    repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    tree = scratch / "tree"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    for part in ("tb", "tests"):
        shutil.copytree(repo / part, tree / part, symlinks=True)
    planner = tree / PLANNER
    original = planner.read_text(encoding="utf-8")
    selftest = [sys.executable, "-B", str(planner), "--self-test"]
    behave = [sys.executable, "-B", "-m", "behave", "tests/features/torture_campaign_plan.feature",
              "-f", "progress", "--no-capture"]
    base_s, base_b = run(selftest, tree), run(behave, tree)
    results = {"baseline": {"selftest_rc": base_s.returncode, "behave_rc": base_b.returncode}}
    print(f"BASELINE selftest rc={base_s.returncode} behave rc={base_b.returncode}")
    if base_s.returncode or base_b.returncode:
        print(base_s.stderr[-2000:], base_b.stdout[-2000:])
        return 2
    rows = []
    for mid, desc, old, new in MUTANTS:
        count = original.count(old)
        if count != 1:
            rows.append((mid, desc, "ANCHOR-ERROR", f"count={count}"))
            print(f"{mid} ANCHOR-ERROR count={count}: {desc}")
            continue
        planner.write_text(original.replace(old, new), encoding="utf-8")
        s = run(selftest, tree)
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", s.stderr, re.M)))
        if s.returncode != 0 and failed:
            verdict, how = "KILLED", "self-test: " + ",".join(failed)
        else:
            b = run(behave, tree)
            m = re.search(r"(\d+) scenarios? passed, (\d+) failed", b.stdout)
            if b.returncode != 0 and m and int(m.group(2)) > 0:
                verdict, how = "KILLED", f"behave only: {m.group(2)} scenario(s) failed"
            else:
                verdict, how = "SURVIVED", f"self-test rc={s.returncode}, behave rc={b.returncode}"
        rows.append((mid, desc, verdict, how))
        print(f"{mid} {verdict}: {desc} [{how}]")
    planner.write_text(original, encoding="utf-8")
    results["mutants"] = [dict(zip(("id", "description", "verdict", "evidence"), r)) for r in rows]
    (scratch / "r362_2_mutants.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    killed = sum(r[2] == "KILLED" for r in rows)
    print(f"SUMMARY killed={killed} survived={sum(r[2] == 'SURVIVED' for r in rows)} "
          f"anchor_errors={sum(r[2] == 'ANCHOR-ERROR' for r in rows)} total={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
