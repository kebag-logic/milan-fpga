#!/usr/bin/env python3
"""Round-4 reviewer mutants on the delta's new grader code; the unchanged self-test must fail each.

Usage: python3 -I r4_reviewer_mutants.py <export root> [jobs]

Each mutant is one exact single-occurrence replacement in a temporary copy of
tb/tools/torture_campaign.py; KILLED means the self-test exits non-zero, and
the failing test names are listed. The export is never written.
"""
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
source = root / "tb/tools/torture_campaign.py"
original = source.read_bytes()
text = original.decode("utf-8")

MUTANTS = (
    ("W01 reading score ignores arms found", "        return dut, -found", "        return dut, 0"),
    ("W02 an equal-score reading replaces the first", "                if score < best[0]:\n                    best = (score, other)\n                continue",
     "                if score <= best[0]:\n                    best = (score, other)\n                continue"),
    ("W03 a flip arm matches a run of any length", '        return event["n"] == 1 and event["mask"] == arm["mask"]',
     '        return event["mask"] == arm["mask"]'),
    ("W04 a masked word after the old track's own keeps the hold",
     "        return xor == self.mask and self.clean is None", "        return xor == self.mask"),
    ("W05 a returned excursion ends at its window's first word",
     "        end = start if image.clean is None else image.clean", "        end = start"),
    ("W06 hold start may split a bit-flip event",
     '            if event["capture_index"] < at < event["capture_index"] + event["n"] and event["class"] == "bit-flip":',
     '            if False:'),
    ("W07 a slip arm splits only at its exact index", "            if abs(at - index) <= steer.tolerance and rest and not rest % AUDIO_BLOCK_FRAMES:",
     "            if at == index and rest and not rest % AUDIO_BLOCK_FRAMES:"),
    ("W08 located_within runs one word past the new track",
     "        while (upto is not None and last + 1 < upto", "        while (upto is not None and last < upto"),
    ("W09 the mask with equal bits set puts the slip first",
     '                len(masks[current]) > 1 or bin(*masks[ahead]).count("1") < bin(*masks[current]).count("1")):',
     '                len(masks[current]) > 1 or bin(*masks[ahead]).count("1") <= bin(*masks[current]).count("1")):'),
    ("W10 upto stops one word short", "    return labels[end - 1][1] + 1\n", "    return labels[end - 1][1]\n"),
    ("W11 the offset before is never remembered", "            held = reference if offset != reference else held\n",
     "            held = held\n"),
    ("W12 a forced word's offset never takes force",
     "            if forced.get(labels[k][1]) not in (None, reference):\n                held, reference = reference, forced[labels[k][1]]\n",
     "            if False:\n                held, reference = reference, forced[labels[k][1]]\n"),
    ("W13 a returned excursion needs the exact old track",
     "            elif back is not None and abs(back) <= abs(final):", "            elif back == 0:"),
    ("W14 the arm-led read never opens before the window",
     "            if index <= track.since or track.start - index > AUDIO_GUARD_FRAMES:",
     "            if True:"),
)


def selftest(body: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory(prefix="r699-4-mut-") as d:
        candidate = Path(d) / source.name
        candidate.write_text(body, encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                              capture_output=True, text=True, timeout=900)


def one(mutant):
    name, old, new = mutant
    if name == "CONTROL":
        r = selftest(text)
        return f"CONTROL pristine rc={r.returncode}"
    if text.count(old) != 1:
        return f"INVALID: {name}: anchor occurs {text.count(old)} times"
    r = selftest(text.replace(old, new))
    failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", r.stderr, re.M)))
    return (f"KILLED: {name} rc={r.returncode} by {failed}" if r.returncode
            else f"SURVIVED: {name} rc=0")


with ThreadPoolExecutor(jobs) as pool:
    lines = list(pool.map(one, (("CONTROL", "", ""),) + MUTANTS))
for line in lines:
    print(line, flush=True)
counts = {k: sum(line.startswith(k) for line in lines) for k in ("KILLED", "SURVIVED", "INVALID")}
print(f"SUMMARY: {len(MUTANTS)} mutants {counts}; export unchanged: {source.read_bytes() == original}")
