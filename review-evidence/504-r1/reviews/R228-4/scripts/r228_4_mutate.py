#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-4 reviewer-owned boundary mutation probes for issue #504 / PR #521.

Usage: r228_4_mutate.py <disposable-tree> <mutant-id> <out-dir> [--sdk <prefix>]

Question: does the resolver control set at 4876423d FAIL when the low
boundary of `_rv32_forget_overlap` (`key[-1] + 3 >= start`) moves in
either direction, and is it the new stale/kept probes that make it fail?

Each mutant is a list of exact-text edits (each anchor must match exactly
once) applied to a DISPOSABLE copy of the tree, which is restored to its
original bytes (SHA-256 re-verified) afterwards. Kinds:

  literal        gate 1b through the compiler-audit wrapper in --absent
                 mode, stopped by a hook planted right after the literal
                 resolver controls (they run on every machine);
  gate1b         the complete gate 1b with the SDK mapped (--sdk-destination);
  gate1b-absent  the complete gate 1b in --absent mode, no hook.

A mutant is KILLED when its control exits non-zero before the hook, and
SURVIVED when the hook (or the whole gate) is reached with exit 0;
any non-zero exit without a failing assertion is a harness ERROR. The
probe label named by the failing assertion is recorded, so which arm
killed it is evidence, not inference.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

BUILDER = "sw/builder/test_builder.py"
AUDIT = "sw/builder/test_firmware_compiler.py"
STOP_ANCHOR = 'f"but stopped at {len(mirror_stops)} non-integer rewrites of it")\n'
STOP_HOOK = (STOP_ANCHOR +
             '    if os.environ.get("R228_STOP_AFTER_LITERALS"):\n'
             '        print("R228-LITERAL-CONTROLS-PASSED", flush=True)\n'
             '        raise SystemExit(0)\n')

LOW = 'key[-1] + 3 >= start]'
HIGH = 'key[-1] <= start + width - 1 and'
#: The four probe entries 4876423d adds, byte-exact as in the source.
STALE_FRAME = r'''        ("a byte store at a frame slot's last byte",
         frame + "\tsw a5,-20(s0)\n\tsb zero,-17(s0)\n\tlw a4,-20(s0)\n"),
'''
STALE_STATIC = r'''        ("a byte store at a static word's last byte",
         static + "\tsw a5,0(a3)\n\tsb zero,3(a3)\n\tlw a4,0(a3)\n"),
'''
KEPT_FRAME = r'''        ("a byte store one past a frame slot's last byte",
         frame + "\tsw a5,-20(s0)\n\tsb zero,-16(s0)\n\tlw a4,-20(s0)\n"),
'''
KEPT_STATIC = r'''        ("a byte store one past a static word's last byte",
         static + "\tsw a5,0(a3)\n\tsb zero,4(a3)\n\tlw a4,0(a3)\n"),
'''


def low(new):
    return (LOW, new)


def drop(entry):
    return (entry, "")


GT = low('key[-1] + 3 > start]')
PLUS4 = low('key[-1] + 4 >= start]')

#: id -> (kind, edits, what it models, expected verdict)
MUTANTS = {
    "null": ("literal", [], "no edit: stop hook only", "SURVIVED"),
    "null-drop-new-probes": (
        "literal", [drop(STALE_FRAME), drop(STALE_STATIC), drop(KEPT_FRAME),
                    drop(KEPT_STATIC)],
        "the four new probes deleted, resolver untouched (the deletion "
        "alone breaks nothing)", "SURVIVED"),
    # ---- the low boundary narrowed: a store at a word's LAST byte keeps it
    "lb-gt": ("literal", [GT], "`+ 3 >= start` -> `+ 3 > start` (the R228-F6 revert)",
              "KILLED"),
    "lb-plus2": ("literal", [low('key[-1] + 2 >= start]')],
                 "`+ 3` -> `+ 2`: same boundary, other spelling", "KILLED"),
    "lb-plus0": ("literal", [low('key[-1] >= start]')],
                 "only words starting at or after the store are forgotten", "KILLED"),
    # ---- the low boundary widened: a store one past a word forgets it
    "lb-plus4": ("literal", [PLUS4], "`+ 3` -> `+ 4` (over-forget)", "KILLED"),
    "lb-ge-start-minus1": ("literal", [low('key[-1] + 3 >= start - 1]')],
                           "`>= start` -> `>= start - 1` (over-forget, other spelling)",
                           "KILLED"),
    "lb-drop": ("literal", [(' and key[-1] + 3 >= start]', ']')],
                "low term removed: every lower word is forgotten", "KILLED"),
    # ---- one caller only (the two callers share the helper)
    "lb-gt-sym-only": ("literal", [low('key[-1] + 3 >= start + (key[0] == "sym")]')],
                       "narrowed for statics only", "KILLED"),
    "lb-gt-frame-only": ("literal", [low('key[-1] + 3 >= start + (key[0] != "sym")]')],
                         "narrowed for frame slots only", "KILLED"),
    "lb-plus4-sym-only": ("literal", [low('key[-1] + 3 + (key[0] == "sym") >= start]')],
                          "widened for statics only", "KILLED"),
    "lb-plus4-frame-only": ("literal", [low('key[-1] + 3 + (key[0] != "sym") >= start]')],
                            "widened for frame slots only", "KILLED"),
    # ---- which probe carries each kill
    "lb-gt-without-new-stale": ("literal", [GT, drop(STALE_FRAME), drop(STALE_STATIC)],
                                "the F6 revert with both new stale probes deleted "
                                "(reproduces the R228-3 gap)", "SURVIVED"),
    "lb-gt-static-stale-alone": ("literal", [GT, drop(STALE_FRAME)],
                                 "the F6 revert, new frame stale probe deleted", "KILLED"),
    "lb-gt-frame-stale-alone": ("literal", [GT, drop(STALE_STATIC)],
                                "the F6 revert, new static stale probe deleted", "KILLED"),
    "lb-gt-sym-only-without-static-stale": (
        "literal", [low('key[-1] + 3 >= start + (key[0] == "sym")]'), drop(STALE_STATIC)],
        "statics narrowed, new static stale probe deleted", "SURVIVED"),
    "lb-gt-frame-only-without-frame-stale": (
        "literal", [low('key[-1] + 3 >= start + (key[0] != "sym")]'), drop(STALE_FRAME)],
        "frame slots narrowed, new frame stale probe deleted", "SURVIVED"),
    "lb-plus4-without-new-kept": ("literal", [PLUS4, drop(KEPT_FRAME), drop(KEPT_STATIC)],
                                  "over-forget with both new kept probes deleted",
                                  "SURVIVED"),
    "lb-plus4-static-kept-alone": ("literal", [PLUS4, drop(KEPT_FRAME)],
                                   "over-forget, new frame kept probe deleted", "KILLED"),
    "lb-plus4-frame-kept-alone": ("literal", [PLUS4, drop(KEPT_STATIC)],
                                  "over-forget, new static kept probe deleted", "KILLED"),
    # ---- the companion high boundary (R228-S8, optional; recorded, not required)
    "hb-lt": ("literal", [(HIGH, 'key[-1] < start + width - 1 and')],
              "a word starting at the store's last byte is kept (R228-S8)", "SURVIVED"),
    "hb-plus1": ("literal", [(HIGH, 'key[-1] <= start + width and')],
                 "a word starting one past the store's last byte is forgotten",
                 "SURVIVED"),
    # ---- R227-3-S1 M17 (optional; recorded, not required)
    "footprint-last-word-short": (
        "literal", [("((address + width - 1) & ~3) + 4, 4)",
                     "((address + width - 2) & ~3) + 4, 4)")],
        "a store's last written word computed one byte short (R227-3-S1 M17)",
        "SURVIVED"),
    # ---- through the complete gate 1b
    "null-gate1b": ("gate1b", [], "pristine head, SDK mapped", "SURVIVED"),
    "null-gate1b-absent": ("gate1b-absent", [], "pristine head, compiler absent",
                           "SURVIVED"),
    "lb-gt-gate1b": ("gate1b", [GT], "the F6 revert, complete gate 1b, SDK mapped",
                     "KILLED"),
    "lb-gt-gate1b-absent": ("gate1b-absent", [GT],
                            "the F6 revert, complete gate 1b, compiler absent", "KILLED"),
    "lb-plus4-gate1b": ("gate1b", [PLUS4], "over-forget, complete gate 1b, SDK mapped",
                        "KILLED"),
}

FAILED_AFTER = re.compile(r"after (.+?) the RV32 resolver")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply(text: str, edits) -> str:
    for old, new in edits:
        count = text.count(old)
        assert count == 1, f"anchor matches {count} times: {old[:60]!r}"
        text = text.replace(old, new)
    return text


def main() -> int:
    tree, ident, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    sdk = sys.argv[sys.argv.index("--sdk") + 1] if "--sdk" in sys.argv else None
    kind, edits, what, expected = MUTANTS[ident]
    target = tree / BUILDER
    original = target.read_bytes()
    before = sha(target)
    mutated = apply(original.decode(), edits)
    env = {}
    if kind == "literal":
        mutated = apply(mutated, [(STOP_ANCHOR, STOP_HOOK)])
        env = {"R228_STOP_AFTER_LITERALS": "1"}
    head = subprocess.run(["git", "-C", str(tree), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    audit = out / f"{ident}.audit.jsonl"
    command = {
        "literal": [sys.executable, "-B", AUDIT, "--absent", "--audit", str(audit)],
        "gate1b": [sys.executable, "-B", AUDIT, "--sdk-destination", str(sdk),
                   "--audit", str(audit)],
        "gate1b-absent": [sys.executable, "-B", AUDIT, "--absent", "--audit", str(audit)],
    }[kind]
    started = time.time()
    try:
        target.write_text(mutated)
        proc = subprocess.run(command, cwd=tree, capture_output=True, text=True,
                              env={**os.environ, **env})
    finally:
        target.write_bytes(original)
    restored = sha(target) == before
    assert restored, f"{ident}: original bytes not restored"
    output = proc.stdout + proc.stderr
    stopped = "R228-LITERAL-CONTROLS-PASSED" in output
    failure = [line for line in output.splitlines()
               if "AssertionError" in line or line.startswith(("FAIL", "ERROR"))
               or "Error:" in line]
    named = sorted({m.group(1) for line in failure for m in FAILED_AFTER.finditer(line)})
    #: KILLED only on a failing assertion of the gate itself; any other
    #: non-zero exit is a harness ERROR and never counts as a kill.
    asserted = any("AssertionError" in line for line in failure)
    if proc.returncode == 0 or stopped:
        verdict = "SURVIVED"
    else:
        verdict = "KILLED" if asserted else "ERROR"
    summary = [line for line in output.splitlines()
               if line.startswith(("GATE 1b", "NOT RUN", "ALL GATES"))][-4:]
    record = {"id": ident, "kind": kind, "tree_head": head, "models": what,
              "edits": [[old, new] for old, new in edits],
              "returncode": proc.returncode, "stop_hook_reached": stopped,
              "verdict": verdict, "expected": expected,
              "as_expected": verdict == expected,
              "killing_probe": named, "first_failure": [f[:400] for f in failure[:2]],
              "gate_summary": summary,
              "seconds": round(time.time() - started, 1),
              "restored_sha256": before, "restored": restored}
    (out / f"{ident}.log").write_text(output)
    (out / f"{ident}.json").write_text(json.dumps(record, indent=1) + "\n")
    print(f"{ident}: {verdict} (expected {expected}) rc={proc.returncode} "
          f"{record['seconds']}s probe={named} {(failure[:1] or [''])[0][:140]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
