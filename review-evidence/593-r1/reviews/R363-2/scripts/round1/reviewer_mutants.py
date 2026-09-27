#!/usr/bin/env python3
"""R363-1 reviewer mutants for the #593 mr/tu soak oracles.

Usage: python3 -B reviewer_mutants.py <repo-root> <scratch-dir>
Copies tb/tools/torture_campaign.py into <scratch-dir>, applies one textual
mutation at a time (anchor must occur exactly once, else INVALID), and runs
the copy's --self-test. KILLED = nonzero exit with a FAIL/ERROR line naming
a test; SURVIVED = rc 0. The repository file is never written.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
source = repo / "tb" / "tools" / "torture_campaign.py"
original = source.read_bytes()
text = original.decode("utf-8")

M = [
    ("M01 mr cause check skipped", "    for toggle in toggles:\n        if not any(",
     "    for toggle in []:\n        if not any("),
    ("M02 mr cause window strict", "                   <= Decimal(str(resolution_s))\n",
     "                   < Decimal(str(resolution_s))\n"),
    ("M03 mr cause window doubled", "                   <= Decimal(str(resolution_s))\n",
     "                   <= 2 * Decimal(str(resolution_s))\n"),
    ("M04 mr cause window one-sided",
     'and abs(Decimal(str(event["timestamp_s"])) - Decimal(str(toggle["timestamp_s"])))',
     'and (Decimal(str(event["timestamp_s"])) - Decimal(str(toggle["timestamp_s"])))'),
    ("M05 mr PDU stream filter removed",
     'stream_pdus = [pdu for pdu in pdus if pdu["stream_id"] == stream_id]', "stream_pdus = pdus"),
    ("M06 MEDIA_RESET read stream filter removed",
     'reads = [read for read in media_reset_reads if read["stream_id"] == stream_id]',
     "reads = media_reset_reads"),
    ("M07 hold threshold 7", 'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 7:'),
    ("M08 hold threshold 9", 'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 9:'),
    ("M09 tail off-by-one strict", 'toggles[-1]["pdu_index"] + 1 < 8:', 'toggles[-1]["pdu_index"] < 8:'),
    ("M10 tail threshold 7", 'toggles[-1]["pdu_index"] + 1 < 8:', 'toggles[-1]["pdu_index"] + 1 < 7:'),
    ("M11 PDU contiguity check removed", 'if (current["pdu_index"] != previous["pdu_index"] + 1\n',
     "if (False\n"),
    ("M12 PDU timestamp order check removed",
     '                or current["timestamp_s"] < previous["timestamp_s"]):\n            return "NOT RUN", {"why": "ordered, contiguous',
     '                or False):\n            return "NOT RUN", {"why": "ordered, contiguous'),
    ("M13 read order check removed", 'if after["timestamp_s"] <= before["timestamp_s"]:', "if False:"),
    ("M14 counter wrap decoding removed", 'delta = (after["value"] - before["value"]) % 2**32',
     'delta = (after["value"] - before["value"])'),
    ("M15 single counter read accepted", "if len(reads) < 2:", "if len(reads) < 1:"),
    ("M16 mr capture_complete ignored",
     "if (capture_complete is not True or not stream_id or pdus is None",
     "if (not stream_id or pdus is None"),
    ("M17 mr negative resolution accepted",
     "            or observation_resolution_s < 0):\n        return \"NOT RUN\", dict(detail, why=\"complete packet",
     "            or False):\n        return \"NOT RUN\", dict(detail, why=\"complete packet"),
    ("M18 mr bit domain unchecked", 'or type(pdu.get("mr")) is not int or pdu["mr"] not in (0, 1)):',
     'or type(pdu.get("mr")) is not int):'),
    ("M19 counter value range unchecked",
     'if type(read.get("value")) is not int or not 0 <= read["value"] < 2**32:',
     'if type(read.get("value")) is not int:'),
    ("M20 cause kind type unchecked", 'if not isinstance(event.get("kind"), str):', "if False:"),
    ("M21 record validation disabled",
     "def _release_mr_records_valid(pdus: list[dict], causes: list[dict], reads: list[dict]) -> bool:\n",
     "def _release_mr_records_valid(pdus: list[dict], causes: list[dict], reads: list[dict]) -> bool:\n    return True\n"),
    ("M22 MEDIA_RESET upper bound drops R",
     'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))',
     'upper_s = Decimal(str(after["timestamp_s"]))'),
    ("M23 MEDIA_RESET lower bound drops R",
     "                   - Decimal(str(resolution_s)))\n", "                   )\n"),
    ("M24 MEDIA_RESET consumes latest", "for event_s in matches_s[:delta]:",
     "for event_s in (matches_s[-delta:] if delta else []):"),
    ("M25 tu GM change not a discontinuity",
     "events_s = [event_s for event_s in discontinuities_s + gm_changes_s if start_s",
     "events_s = [event_s for event_s in discontinuities_s if start_s"),
    ("M26 tu GM change at clear counted", "gm_events_s = [event_s for event_s in gm_changes_s if event_s < clear_s]",
     "gm_events_s = [event_s for event_s in gm_changes_s if event_s <= clear_s]"),
    ("M27 tu GM minimum 0.24", 'max(gm_events_s) + Decimal("0.25")', 'max(gm_events_s) + Decimal("0.24")'),
    ("M28 tu any holdover bound accepted", "clear_s <= observed_start_s or holdover_bound_s != 0.5",
     "clear_s <= observed_start_s or holdover_bound_s <= 0"),
    ("M29 tu zero-length interval accepted", "clear_s <= observed_start_s or holdover_bound_s != 0.5",
     "clear_s < observed_start_s or holdover_bound_s != 0.5"),
    ("M31 exit_code NOT RUN not soft",
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN", "NOT RUN") for r in records)',
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN") for r in records)'),
    ("M32 release evidence text drops NOT RUN", "missing, NOT RUN, SKIP, INFO, ", "missing, SKIP, INFO, "),
    ("M33 mr assertion drops GM-alone", "GM change alone fails; ", ""),
    ("M34 mr assertion drops interval counting", '"MEDIA_RESET counts observation intervals, not packets; "', '""'),
    ("M35 plan cause kinds drop CRF toggle",
     'mr_cause_kinds=["media-clock-source change", "CRF disruption", "CRF mr toggle"],',
     'mr_cause_kinds=["media-clock-source change", "CRF disruption"],'),
    ("M36 plan evidence drops gm_changes", '"MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes"],',
     '"MEDIA_RESET_reads", "gptp_discontinuities"],'),
    ("M37 plan counter bound 2 s", "mr_counter_update_bound_s=MILAN_MAX_OBSERVATION_INTERVAL_S,",
     "mr_counter_update_bound_s=2,"),
    ("M39 falling toggles ignored", 'if current["mr"] != previous["mr"]:', 'if current["mr"] > previous["mr"]:'),
    ("M40 first toggle exempt from cause", "    for toggle in toggles:\n        if not any(",
     "    for toggle in toggles[1:]:\n        if not any("),
    ("M41 last toggle exempt from cause", "    for toggle in toggles:\n        if not any(",
     "    for toggle in toggles[:-1]:\n        if not any("),
    ("M43 one extra uncaused increment tolerated", "if delta > len(matches_s):", "if delta > len(matches_s) + 1:"),
    ("M45 counter check skipped without toggles", '    if verdict != "PASS":\n        return verdict, detail\n    verdict, evidence = _release_media_resets(',
     '    if verdict != "PASS" or not detail["toggles_s"]:\n        return verdict, detail\n    verdict, evidence = _release_media_resets('),
    ("M46 tu verdict drops resolution field", '    detail = {"observation_resolution_s": observation_resolution_s}\n    if (capture_complete is not True or gm_changes_s is None',
     '    detail = {}\n    if (capture_complete is not True or gm_changes_s is None'),
    ("M47 mr verdict drops resolution field",
     'detail = {"stream_id": stream_id, "observation_resolution_s": observation_resolution_s,',
     'detail = {"stream_id": stream_id,'),
    ("M48 tu GM minimum ignores GM before start",
     "gm_events_s = [event_s for event_s in gm_changes_s if event_s < clear_s]",
     "gm_events_s = [event_s for event_s in gm_changes_s if observed_start_s <= event_s < clear_s]"),
]

clean_dir = work / "clean"
clean_dir.mkdir(exist_ok=True)
(clean_dir / source.name).write_bytes(original)
cmd = lambda p: [sys.executable, "-B", str(p), "--self-test"]
base = subprocess.run(cmd(clean_dir / source.name), capture_output=True, text=True, timeout=600)
print(f"BASELINE rc={base.returncode} ok={'OK' in base.stderr.splitlines()[-1:]}")
if base.returncode != 0:
    sys.exit(1)
tally = {"KILLED": 0, "SURVIVED": 0, "INVALID": 0}
for name, old, new in M:
    count = text.count(old)
    if count != 1:
        print(f"INVALID: {name}: anchor count {count}")
        tally["INVALID"] += 1
        continue
    mdir = work / re.sub(r"[^A-Za-z0-9]+", "_", name)
    mdir.mkdir(exist_ok=True)
    (mdir / source.name).write_text(text.replace(old, new), encoding="utf-8")
    r = subprocess.run(cmd(mdir / source.name), capture_output=True, text=True, timeout=600)
    failing = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", r.stderr, re.M)))
    status = "KILLED" if r.returncode != 0 and failing else ("SURVIVED" if r.returncode == 0 else "KILLED(no-name)")
    tally[status.split("(")[0]] = tally.get(status.split("(")[0], 0) + 1
    print(f"{status}: {name}: rc={r.returncode} tests={failing}")
if source.read_bytes() != original:
    raise SystemExit("repository planner changed")
print("TALLY", tally, "repository source unchanged")
