#!/usr/bin/env python3
"""Mutation probes for the overlap low-boundary control (R227-3, R228-F6).

usage: a194_mutate.py <source-tree> <work-dir> <receipt-dir> <id> [<id> ...]
       [--sdk <destination>] [--full]

Each probe copies <source-tree> (no .git, no __pycache__) into
<work-dir>/<id>, applies exact-string edits (each asserted to apply exactly
once), and runs gate 1b through sw/builder/test_firmware_compiler.py.
Without --full a stop marker is planted right after the stale/kept literal
probes, so a run that reaches it proves every literal resolver control up to
that point passed.  The verdict is read from the gate's own assertion
sentence or from the stop marker.  The copy is deleted afterwards.
"""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

TARGET = "sw/builder/test_builder.py"
STOP = "A194-STOP-MARKER: every literal resolver control up to here passed"
ANCHOR_STOP = "    store_classes_note = (\n"
LOW = "key[-1] <= start + width - 1 and key[-1] + 3 >= start]"
FRAME_STALE = ('        ("a byte store at a frame slot\'s last byte",\n'
               '         frame + "\\tsw a5,-20(s0)\\n\\tsb zero,-17(s0)\\n'
               '\\tlw a4,-20(s0)\\n"),\n')
STATIC_STALE = ('        ("a byte store at a static word\'s last byte",\n'
                '         static + "\\tsw a5,0(a3)\\n\\tsb zero,3(a3)\\n'
                '\\tlw a4,0(a3)\\n"),\n')
FRAME_KEPT = ('        ("a byte store one past a frame slot\'s last byte",\n'
              '         frame + "\\tsw a5,-20(s0)\\n\\tsb zero,-16(s0)\\n'
              '\\tlw a4,-20(s0)\\n"),\n')

M1 = (LOW, LOW.replace("+ 3 >= start", "+ 3 > start"))
M2 = (LOW, LOW.replace("+ 3 >= start", "+ 4 >= start"))

#: id -> (edits, expected verdict, expected sentence fragment)
PROBES = {
    "M0-none": ([], "STOP", None),
    "M1-overlap-last-byte": (
        [M1], "KILLED",
        "after a byte store at a frame slot's last byte the RV32 resolver "
        "still placed the next store"),
    "M1s-overlap-last-byte-static-probe-alone": (
        [M1, (FRAME_STALE, "")], "KILLED",
        "after a byte store at a static word's last byte the RV32 resolver "
        "still placed the next store"),
    "M1x-overlap-last-byte-without-new-probes": (
        [M1, (FRAME_STALE, ""), (STATIC_STALE, "")], "STOP", None),
    "M2-overlap-over-forget": (
        [M2], "KILLED",
        "after a byte store one past a frame slot's last byte the RV32 "
        "resolver reported the next store as [unplaced("),
    "M2s-overlap-over-forget-static-arm-alone": (
        [M2, (FRAME_KEPT, "")], "KILLED",
        "after a byte store one past a static word's last byte the RV32 "
        "resolver reported the next store as [unplaced("),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    argv = sys.argv[1:]
    sdk = None
    full = "--full" in argv
    if full:
        argv.remove("--full")
    if "--sdk" in argv:
        at = argv.index("--sdk")
        sdk = argv[at + 1]
        del argv[at:at + 2]
    source, work, receipts = (Path(arg).resolve() for arg in argv[:3])
    ids = argv[3:]
    receipts.mkdir(parents=True, exist_ok=True)
    source_sha = sha256(source / TARGET)
    failures = 0
    for probe in ids:
        edits, expect, sentence = PROBES[probe]
        tag = probe + ("-full" if full else "") + ("-sdk" if sdk else "-absent")
        tree = work / tag
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(source, tree, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        target = tree / TARGET
        text = target.read_text()
        applied = []
        for old, new in edits + ([] if full else
                                 [(ANCHOR_STOP, f"    raise SystemExit({STOP!r})\n"
                                   + ANCHOR_STOP)]):
            count = text.count(old)
            assert count == 1, f"{probe}: anchor applies {count} times: {old!r}"
            text = text.replace(old, new)
            applied.append({"old": old, "new": new})
        target.write_text(text)
        mode = ["--sdk-destination", sdk] if sdk else ["--absent"]
        audit = work / f"{tag}.audit.jsonl"
        started = time.monotonic()
        run = subprocess.run(
            [sys.executable, "-B", "-u", str(tree / "sw/builder/test_firmware_compiler.py"),
             *mode, "--audit", str(audit)],
            cwd=tree, capture_output=True, text=True)
        elapsed = round(time.monotonic() - started, 1)
        output = run.stdout + run.stderr
        (receipts / f"{tag}.log").write_text(output)
        stopped = STOP in output
        passed = run.returncode == 0 and "GATE 1b PASS" in output
        if stopped or passed:
            verdict = "STOP" if stopped else "PASS"
        elif sentence and sentence in output:
            verdict = "KILLED"
        else:
            verdict = "OTHER-FAILURE"
        want = "PASS" if (full and expect == "STOP") else expect
        ok = verdict == want
        failures += not ok
        record = {
            "probe": tag, "source_tree": str(source),
            "source_target_sha256": source_sha,
            "mutated_target_sha256": sha256(target), "edits": applied,
            "stop_marker_planted": not full, "sdk_destination": sdk,
            "exit": run.returncode, "seconds": elapsed, "verdict": verdict,
            "expected": want, "as_expected": ok,
            "expected_sentence": sentence,
            "last_lines": output.strip().splitlines()[-6:],
        }
        (receipts / f"{tag}.json").write_text(json.dumps(record, indent=2) + "\n")
        print(f"{tag}: exit {run.returncode}, {elapsed}s, {verdict} "
              f"(expected {want}){'' if ok else '  <-- UNEXPECTED'}", flush=True)
        shutil.rmtree(tree)
    assert sha256(source / TARGET) == source_sha, "source tree was modified"
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
