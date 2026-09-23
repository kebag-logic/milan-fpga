#!/usr/bin/env python3
"""R227-4 overlap-boundary mutation probe for PR #521 at 4876423d.

Usage: overlap_probe.py <exact-head tree> <work dir> [probe ...]

Each probe copies <tree>/sw/builder/test_builder.py into a private copy of
the tree under <work dir>/<probe>, applies exact-string edits (each asserted
to occur exactly once), imports the mutated module in a fresh interpreter and
executes the literal resolver control segment of
test_baremetal_profile_contract() verbatim: the `rv32_probe` helper and the
source from `outside = 0x8000_1000` up to `store_classes_note = (`, i.e. the
stale-probe and kept-probe loops with their own assertion sentences. The
verdict is the first AssertionError sentence (KILLED) or SURVIVED. The
segment is read from the mutated file itself, so a probe that deletes a
control deletes it from what runs.
"""

import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

FORGET_LOW = "key[-1] <= start + width - 1 and key[-1] + 3 >= start]"
FRAME_STALE = ("        (\"a byte store at a frame slot's last byte\",\n"
               "         frame + \"\\tsw a5,-20(s0)\\n\\tsb zero,-17(s0)\\n"
               "\\tlw a4,-20(s0)\\n\"),\n")
STATIC_STALE = ("        (\"a byte store at a static word's last byte\",\n"
                "         static + \"\\tsw a5,0(a3)\\n\\tsb zero,3(a3)\\n"
                "\\tlw a4,0(a3)\\n\"),\n")
FRAME_KEPT = ("        (\"a byte store one past a frame slot's last byte\",\n"
              "         frame + \"\\tsw a5,-20(s0)\\n\\tsb zero,-16(s0)\\n"
              "\\tlw a4,-20(s0)\\n\"),\n")
STATIC_KEPT = ("        (\"a byte store one past a static word's last byte\",\n"
               "         static + \"\\tsw a5,0(a3)\\n\\tsb zero,4(a3)\\n"
               "\\tlw a4,0(a3)\\n\"),\n")


def low(new: str) -> tuple[str, str]:
    """Replace the whole overlap condition with `new`."""
    return (FORGET_LOW, new)


PROBES = {
    "P0-head": [],
    # Low boundary, under-forget: the reported gap.
    "M1-gt": [low("key[-1] <= start + width - 1 and key[-1] + 3 > start]")],
    "M1-gt-no-frame-stale": [
        low("key[-1] <= start + width - 1 and key[-1] + 3 > start]"),
        (FRAME_STALE, "")],
    "M1-gt-no-new-stale": [
        low("key[-1] <= start + width - 1 and key[-1] + 3 > start]"),
        (FRAME_STALE, ""), (STATIC_STALE, "")],
    "M1-plus2": [low("key[-1] <= start + width - 1 and key[-1] + 2 >= start]")],
    "M1-plus1": [low("key[-1] <= start + width - 1 and key[-1] + 1 >= start]")],
    "M1-plus2-no-new-stale": [
        low("key[-1] <= start + width - 1 and key[-1] + 2 >= start]"),
        (FRAME_STALE, ""), (STATIC_STALE, "")],
    # Low boundary, over-forget: pinned by the kept arm.
    "M2-plus4": [low("key[-1] <= start + width - 1 and key[-1] + 4 >= start]")],
    "M2-plus4-no-frame-kept": [
        low("key[-1] <= start + width - 1 and key[-1] + 4 >= start]"),
        (FRAME_KEPT, "")],
    "M2-plus4-no-new-kept": [
        low("key[-1] <= start + width - 1 and key[-1] + 4 >= start]"),
        (FRAME_KEPT, ""), (STATIC_KEPT, "")],
    "M2-plus3-start-minus1": [
        low("key[-1] <= start + width - 1 and key[-1] + 3 >= start - 1]")],
    "M2-plus7": [low("key[-1] <= start + width - 1 and key[-1] + 7 >= start]")],
    # Low term dropped entirely (every lower key forgotten).
    "M3-low-term-dropped": [low("key[-1] <= start + width - 1]")],
    "M3-low-term-dropped-no-new-kept": [
        low("key[-1] <= start + width - 1]"),
        (FRAME_KEPT, ""), (STATIC_KEPT, "")],
    # Companion HIGH boundary (outside this delta; prior optional suggestion).
    "U1-high-lt": [low("key[-1] < start + width - 1 and key[-1] + 3 >= start]")],
    "U2-high-plus-width": [
        low("key[-1] <= start + width and key[-1] + 3 >= start]")],
    "U3-high-term-dropped": [low("key[-1] + 3 >= start]")],
}

RUNNER = r'''
import json, sys, textwrap
sys.path.insert(0, sys.argv[1])
import test_builder as tb
src = open(sys.argv[2], encoding="utf-8").read()
helper_at = src.index("    def rv32_probe(body: str)")
helper_end = src.index("    for label, base, insn, words in class_probes:")
seg_at = src.index("    outside = 0x8000_1000\n")
seg_end = src.index("    store_classes_note = (")
code = textwrap.dedent(src[helper_at:helper_end]) + textwrap.dedent(src[seg_at:seg_end])
ns = dict(vars(tb))
verdict = {"stale": None, "kept": None}
try:
    exec(compile(code, "literal-control-segment", "exec"), ns)
except AssertionError as exc:
    verdict["result"] = "KILLED"
    verdict["sentence"] = str(exc)
else:
    verdict["result"] = "SURVIVED"
    verdict["sentence"] = None
verdict["stale"] = len(ns.get("stale_probes", ()))
verdict["kept"] = len(ns.get("kept_probes", ()))
print(json.dumps(verdict))
'''


def run_probe(tree: Path, work: Path, name: str) -> dict:
    """Mutate a private copy and run the literal control segment."""
    edits = PROBES[name]
    root = work / name
    builder = root / "sw" / "builder"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(tree / "sw" / "builder", builder)
    for sub in ("scripts", "avdecc", "sw/litex", "configs"):
        link = root / sub
        link.parent.mkdir(parents=True, exist_ok=True)
        if not link.exists():
            link.symlink_to((tree / sub).resolve())
    target = builder / "test_builder.py"
    text = target.read_text(encoding="utf-8")
    for old, new in edits:
        count = text.count(old)
        assert count == 1, f"{name}: edit anchor occurs {count} times: {old!r}"
        text = text.replace(old, new)
    target.write_text(text, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-B", "-c", RUNNER, str(builder), str(target)],
        capture_output=True, text=True, timeout=600, check=False)
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    result = json.loads(lines[-1]) if lines else {
        "result": "ERROR", "sentence": proc.stderr[-2000:]}
    result.update(probe=name, edits=len(edits), exit=proc.returncode)
    return result


def main() -> None:
    """Run the named (or all) probes and print one JSON line each."""
    tree, work = Path(sys.argv[1]), Path(sys.argv[2])
    names = sys.argv[3:] or list(PROBES)
    for name in names:
        print(json.dumps(run_probe(tree, work, name)), flush=True)


if __name__ == "__main__":
    main()
