#!/usr/bin/env python3
"""Reviewer mutants on the round-3 delta of the #396 audio grader.

Usage: python3 -I r3_reviewer_mutants.py <export root> [jobs]

Each mutant is one exact single-occurrence replacement in a private copy of
tb/tools/torture_campaign.py; it is KILLED when the planner self-test exits
non-zero. A pristine control must pass. The export is never written.
"""
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
source = root / "tb/tools/torture_campaign.py"
text = source.read_text(encoding="utf-8")
MUTANTS = (
    ("V01 qualified start without its guard",
     "start = max(slot.acquired for slot in self.slots.values()) + AUDIO_GUARD_FRAMES",
     "start = max(slot.acquired for slot in self.slots.values())"),
    ("V02 qualified end without its guard",
     "return start, max(start, frames - AUDIO_GUARD_FRAMES)", "return start, max(start, frames)"),
    ("V03 arms outside the interval accepted",
     "if any(not start <= arm[\"index\"] < end for arm in log.planted_arms):",
     "if False and any(not start <= arm[\"index\"] < end for arm in log.planted_arms):"),
    ("V04 losses outside the interval accepted",
     "if any(not start <= loss[\"index\"] < end for loss in log.capture_losses):",
     "if False and any(not start <= loss[\"index\"] < end for loss in log.capture_losses):"),
    ("V05 required length off by one frame",
     "if end - start < required_s * layout.rate_hz:", "if end - start + 1 < required_s * layout.rate_hz:"),
    ("V06 no early refusal of an unacquired channel",
     "if index > AUDIO_WINDOW_WORDS and scan.unacquired():", "if False and scan.unacquired():"),
    ("V07 per-word hold release removed",
     "if slot.image is not None and word ^ slot.image.due(index) != slot.image.mask:",
     "if False and slot.image is not None:"),
    ("V08 fast-path hold release removed",
     "if slot.image is not None and not slot.image.holds(first, column):",
     "if False and slot.image is not None:"),
    ("V09 return needs the exact mask",
     "and found[1] == image.tag and mask in (0, image.mask)", "and found[1] == image.tag and mask == image.mask"),
    ("V10 window bound no longer keeps a constant mask",
     "if back is None and end == len(labels) and end - k > 1 and track.reason == AUDIO_BOUND_REASON:",
     "if False:"),
    ("V11 open words at the end start one later",
     "first, last = (wrong[0], wrong[-1]) if track.acquiring else (wrong[0], end - 1)",
     "first, last = (wrong[0], wrong[-1]) if track.acquiring else (wrong[0] + 1, end - 1)"),
    ("V12 open location bound at the end widened",
     "bounds = [max(first - AUDIO_GUARD_FRAMES + 1, stretch), first]",
     "bounds = [max(first - AUDIO_GUARD_FRAMES, stretch), first]"),
    ("V13 half-block candidate dropped",
     "for offset in (near, near - AUDIO_BLOCK_FRAMES) if delta == AUDIO_BLOCK_FRAMES // 2 else (near,):",
     "for offset in (near,):"),
    ("V14 unobserved frames counted as observed",
     "return {\"start\": start, \"end\": end, \"frames\": end - start,",
     "return {\"start\": start, \"end\": end, \"frames\": end - start + sum(loss[\"frames\"] for loss in losses),"),
    ("V15 anchor gap after the last anchor omitted",
     "return gaps + ([[marks[-1], frames]] if marks[-1] != frames else [])", "return gaps"),
    ("V16 held events released with no reason at the end",
     "                self._release(channel, \"the capture ended inside a constant-mask excursion\")\n        spans",
     "                self._release(channel, None)\n        spans"),
)


def selftest(body):
    with tempfile.TemporaryDirectory(prefix="r699-r3mut-") as d:
        candidate = Path(d) / source.name
        candidate.write_text(body, encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(candidate), "--self-test"],
                              capture_output=True, text=True, timeout=900)


control = selftest(text)
print(f"CONTROL pristine rc={control.returncode}", flush=True)


def one(m):
    name, old, new = m
    if text.count(old) != 1:
        return f"INVALID: {name} (anchor count {text.count(old)})"
    r = selftest(text.replace(old, new))
    failing = [l.split(" ")[1] for l in r.stderr.splitlines() if l.startswith(("FAIL: ", "ERROR: "))]
    return (f"KILLED: {name} rc={r.returncode} by {sorted(set(failing))[:4]}" if r.returncode
            else f"SURVIVED: {name}")


with ThreadPoolExecutor(jobs) as pool:
    for line in pool.map(one, MUTANTS):
        print(line, flush=True)
