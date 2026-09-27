#!/usr/bin/env python3
"""R362-1 reviewer mutants for the #593 checks in tb/tools/torture_campaign.py.

Usage: reviewer_mutants.py /path/to/checkout WORKDIR
Copies the planner into WORKDIR per mutant (the checkout is never written),
applies one exact single-occurrence substitution, runs the unchanged
`--self-test`, and records KILLED (rc != 0) or SURVIVED (rc == 0).
Runs at most 8 jobs in parallel. Prints one line per mutant and a summary.
"""
import concurrent.futures
import hashlib
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
source = root / "tb/tools/torture_campaign.py"
text = source.read_text(encoding="utf-8")
digest = hashlib.sha256(source.read_bytes()).hexdigest()

# id, description, old, new
MUTANTS = (
    ("R01", "mr cause window doubled",
     "<= Decimal(str(resolution_s))\n                   for event in causes",
     "<= 2 * Decimal(str(resolution_s))\n                   for event in causes"),
    ("R02", "mr cause window made exclusive",
     "<= Decimal(str(resolution_s))\n                   for event in causes",
     "< Decimal(str(resolution_s))\n                   for event in causes"),
    ("R03", "mr cause window one-sided (cause must precede toggle)",
     'abs(Decimal(str(event["timestamp_s"])) - Decimal(str(toggle["timestamp_s"])))',
     '(Decimal(str(toggle["timestamp_s"])) - Decimal(str(event["timestamp_s"])))'),
    ("R04", "mr hold threshold 7",
     'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 7:'),
    ("R05", "mr hold threshold 9",
     'if current["pdu_index"] - previous["pdu_index"] < 8:',
     'if current["pdu_index"] - previous["pdu_index"] < 9:'),
    ("R06", "mr tail off by one",
     'if toggles and pdus[-1]["pdu_index"] - toggles[-1]["pdu_index"] + 1 < 8:',
     'if toggles and pdus[-1]["pdu_index"] - toggles[-1]["pdu_index"] < 8:'),
    ("R07", "mr contiguity check removed",
     'if (current["pdu_index"] != previous["pdu_index"] + 1\n                or current["timestamp_s"] < previous["timestamp_s"]):',
     'if (current["timestamp_s"] < previous["timestamp_s"]):'),
    ("R08", "mr PDU timestamp order check removed",
     'if (current["pdu_index"] != previous["pdu_index"] + 1\n                or current["timestamp_s"] < previous["timestamp_s"]):',
     'if (current["pdu_index"] != previous["pdu_index"] + 1):'),
    ("R09", "mr PDU stream filter removed",
     'stream_pdus = [pdu for pdu in pdus if pdu["stream_id"] == stream_id]',
     "stream_pdus = pdus"),
    ("R10", "MEDIA_RESET read stream filter removed",
     'reads = [read for read in media_reset_reads if read["stream_id"] == stream_id]',
     "reads = media_reset_reads"),
    ("R11", "MEDIA_RESET endpoint requirement relaxed to one read",
     "if len(reads) < 2:", "if len(reads) < 1:"),
    ("R12", "MEDIA_RESET read order check removed",
     'if after["timestamp_s"] <= before["timestamp_s"]:', "if False:"),
    ("R13", "MEDIA_RESET wrap decode removed",
     'delta = (after["value"] - before["value"]) % 2**32',
     'delta = after["value"] - before["value"]'),
    ("R14", "MEDIA_RESET lower window drops R",
     '- Decimal(str(resolution_s)))\n        upper_s',
     ')\n        upper_s'),
    ("R15", "MEDIA_RESET upper window drops R",
     'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))',
     'upper_s = Decimal(str(after["timestamp_s"]))'),
    ("R16", "MEDIA_RESET upper window widened by 1 s",
     'upper_s = Decimal(str(after["timestamp_s"])) + Decimal(str(resolution_s))',
     'upper_s = Decimal(str(after["timestamp_s"])) + 1 + Decimal(str(resolution_s))'),
    ("R17", "MEDIA_RESET consumes latest matches",
     "for event_s in matches_s[:delta]:", "for event_s in matches_s[len(matches_s) - delta:]:"),
    ("R18", "MEDIA_RESET check skipped after toggle pass",
     'verdict, evidence = _release_media_resets(reads, detail["toggles_s"], observation_resolution_s)',
     'verdict, evidence = "PASS", {"media_reset_increments": 0}'),
    ("R19", "mr record validation bypassed",
     "if not _release_mr_records_valid(pdus, causes, media_reset_reads):", "if False:"),
    ("R20", "mr capture_complete ignored",
     "if (capture_complete is not True or not stream_id or pdus is None",
     "if (not stream_id or pdus is None"),
    ("R21", "mr negative resolution accepted",
     "            or observation_resolution_s < 0):\n        return \"NOT RUN\", dict(detail, why=\"complete packet",
     "            ):\n        return \"NOT RUN\", dict(detail, why=\"complete packet"),
    ("R22", "tu GM changes not counted as discontinuities",
     "for event_s in discontinuities_s + gm_changes_s if start_s <= event_s < clear_s]",
     "for event_s in discontinuities_s if start_s <= event_s < clear_s]"),
    ("R23", "tu GM minimum 0.24 s",
     'max(gm_events_s) + Decimal("0.25")', 'max(gm_events_s) + Decimal("0.24")'),
    ("R24", "tu GM minimum considers GM changes at or after clear",
     "gm_events_s = [event_s for event_s in gm_changes_s if event_s < clear_s]",
     "gm_events_s = [event_s for event_s in gm_changes_s if event_s <= clear_s + 1]"),
    ("R25", "tu GM minimum strict comparison",
     "clear_s + observation_resolution_s < minimum_clear_s", "clear_s + observation_resolution_s <= minimum_clear_s"),
    ("R26", "tu 0.5 s bound guard removed",
     "holdover_bound_s != 0.5 or", "False or"),
    ("R27", "tu zero-length interval accepted",
     "if clear_s <= observed_start_s or", "if clear_s < observed_start_s or"),
    ("R28", "NOT RUN no longer outstanding in exit code",
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN", "NOT RUN") for r in records)',
     'soft = any(r["verdict"] in ("FAIL", "NEEDS-HUMAN") for r in records)'),
    ("R29", "tu assertion drops the GM minimum text",
     '"after each GM change, clear + observation_resolution_s must be at least "\n               '
     '"GM change + 0.25 s (Annex B.1.1 minimum); missing GM history is NOT RUN; clock validity "',
     '"clock validity "'),
    ("R30", "mr assertion drops MEDIA_RESET interval semantics",
     '"MEDIA_RESET counts observation intervals, not packets; "', '""'),
    ("R31", "release evidence text drops NOT RUN",
     '"need measured PASS records on the exact image; missing, NOT RUN, SKIP, INFO, "',
     '"need measured PASS records on the exact image; missing, SKIP, INFO, "'),
    ("R32", "plan cause kinds drop CRF mr toggle",
     'mr_cause_kinds=["media-clock-source change", "CRF disruption", "CRF mr toggle"],',
     'mr_cause_kinds=["media-clock-source change", "CRF disruption"],'),
    ("R33", "plan cause window becomes a literal",
     'mr_cause_window="toggle timestamp +/- observation_resolution_s",',
     'mr_cause_window="toggle timestamp +/- 0.01 s",'),
    ("R34", "plan continuous evidence drops gm_changes",
     '"MEDIA_RESET_reads", "gptp_discontinuities", "gm_changes"],\n                mr_oracle',
     '"MEDIA_RESET_reads", "gptp_discontinuities"],\n                mr_oracle'),
    ("R35", "mr GM time-source change accepted as cause",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle", "GM time-source change"}'),
    ("R36", "mr PHC step accepted as cause",
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle"}',
     'allowed = {"media-clock-source change", "CRF disruption", "CRF mr toggle", "PHC settime/adjtime"}'),
)


def run(mutant):
    ident, name, old, new = mutant
    count = text.count(old)
    if count != 1:
        return ident, name, f"INVALID(anchor x{count})", ""
    directory = work / ident
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / "torture_campaign.py"
    candidate.write_text(text.replace(old, new), encoding="utf-8")
    result = subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                            capture_output=True, text=True, timeout=600)
    failed = sorted({line.split()[1] for line in result.stderr.splitlines()
                     if line.startswith(("FAIL: ", "ERROR: "))})
    return ident, name, "KILLED" if result.returncode != 0 else "SURVIVED", ",".join(failed)


print(f"planner sha256 {digest}")
work.mkdir(parents=True, exist_ok=True)
baseline = work / "baseline"
baseline.mkdir(exist_ok=True)
(baseline / "torture_campaign.py").write_text(text, encoding="utf-8")
clean = subprocess.run([sys.executable, "-B", str(baseline / "torture_campaign.py"), "--self-test"],
                       capture_output=True, text=True, timeout=600)
print(f"baseline rc={clean.returncode}")
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, MUTANTS))
for ident, name, status, tests in results:
    print(f"{ident} | {status} | {name} | {tests}")
counts = {}
for _, _, status, _ in results:
    counts[status.split("(")[0]] = counts.get(status.split("(")[0], 0) + 1
print("SUMMARY", counts)
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, "checkout planner changed"
print("checkout planner unchanged")
