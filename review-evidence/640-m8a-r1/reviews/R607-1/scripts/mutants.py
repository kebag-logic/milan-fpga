#!/usr/bin/env python3
"""R607-1 mutation probes for PR #721 (sw/litex/ctrl_memory.py, milan_soc.CtrlMemory).

Each mutant copies sw/ of a pristine tree (other top-level entries symlinked) into its own
directory under OUT, applies one exact textual edit (which must match exactly
once), runs sw/litex/test_ctrl_memory.py there with the LiteX interpreter, and
records rc plus the FAIL lines. The pristine tree is never edited.

    python3 mutants.py <pristine-tree> <out-dir> <litex-python> [--jobs N]
"""
from __future__ import annotations

import argparse
import concurrent.futures
import os
import shutil
import subprocess
import sys
from pathlib import Path

MEM = "sw/litex/ctrl_memory.py"
SOC = "sw/litex/milan_soc.py"
MUTANTS = {
    # name: (file, old, new, what the defect is)
    "budget_slack_1p5": (MEM, "if need.tiles > budget:", "if need.tiles > budget + 1.5:",
                         "budget check admits up to 57.5 RAMB36"),
    "budget_ge": (MEM, "if need.tiles > budget:", "if need.tiles >= budget:",
                  "budget check refuses exactly 56 RAMB36 (ruling: up to 56)"),
    "nobits_in_rom_off": (MEM, "if not s.loaded and home is rom:", "if False:",
                          "a NOBITS section in rom is accepted"),
    "lma_overlap_off": (MEM, '    _overlap("initial bytes", ', '    0 and _overlap("initial bytes", ',
                        "two sections sharing a load address are accepted"),
    "no_bytes_at_entry_off": (MEM, "if not any(s.loaded and s.vma <= image.entry", "if False and not any(s.loaded and s.vma <= image.entry",
                              "an image with no initial bytes at the reset address is accepted"),
    "regions_overlap_off": (MEM, '    _overlap("regions", ', '    0 and _overlap("regions", ',
                            "overlapping regions accepted"),
    "lma_identity": (MEM, "return paddr + vma - vaddr", "return vma",
                     "load addresses read as virtual addresses"),
    "stage_lt": (MEM, "if size != stage:", "if size < stage:",
                 "a larger staging buffer accepted"),
    "low_minus1": (SOC, "low = (region.size - 1).bit_length() - 2", "low = (region.size - 1).bit_length() - 3",
                   "decode one word-address bit short: the top of the region aliases banks"),
    "hole_gt": (SOC, "slaves.append((lambda a: a[:low] >= first, hole))", "slaves.append((lambda a: a[:low] > first, hole))",
                "the first word past the last bank answers nothing"),
    "rom_init_offset": (SOC, "words[first:first + depth]", "words[0:depth]",
                        "every rom bank initialised from the image start"),
    "err_held": (SOC, "hole.err.eq(hole.cyc & hole.stb & ~hole.err)", "hole.err.eq(hole.cyc & hole.stb)",
                 "the hole holds err for a second cycle"),
}


def run(name: str, pristine: Path, out: Path, python: str) -> tuple[str, int, list[str]]:
    """Build one mutant tree, run the test, return (name, rc, FAIL lines)."""
    path, old, new, _ = MUTANTS[name]
    tree = out / name
    tree.mkdir()
    for entry in pristine.iterdir():
        if entry.name == "sw":
            shutil.copytree(entry, tree / "sw", symlinks=True)
        elif entry.name != ".git":
            (tree / entry.name).symlink_to(entry)   # read-only use; only sw/ is edited
    target = tree / path
    text = target.read_text()
    if text.count(old) != 1:
        return name, -1, [f"edit does not match exactly once ({text.count(old)})"]
    target.write_text(text.replace(old, new))
    env = dict(os.environ)
    log = out / f"{name}.log"
    with log.open("w") as fh:
        rc = subprocess.run([python, str(tree / "sw/litex/test_ctrl_memory.py")], cwd=tree,
                            stdout=fh, stderr=subprocess.STDOUT, env=env, timeout=600).returncode
    fails = [ln for ln in log.read_text().splitlines() if ln.startswith("FAIL:")]
    return name, rc, fails


def main() -> int:
    """Run every mutant and print a verdict table."""
    ap = argparse.ArgumentParser()
    ap.add_argument("pristine", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("python")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    args.pristine, args.out = args.pristine.resolve(), args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    rows = []
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        for name, rc, fails in pool.map(lambda n: run(n, args.pristine, args.out, args.python), MUTANTS):
            text = (args.out / f"{name}.log").read_text() if rc >= 0 else ""
            if rc == 1 and "RESULT: FAIL" in text and fails:
                verdict = "KILLED"
            elif rc == 0 and "RESULT: PASS" in text:
                verdict = "SURVIVED"
            else:
                verdict = f"ERROR rc={rc}"
            rows.append((name, verdict, MUTANTS[name][3], fails))
    for name, verdict, what, fails in rows:
        print(f"{name}\t{verdict}\t{what}\t{len(fails)} FAIL line(s)")
        for line in fails[:3]:
            print(f"    {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
