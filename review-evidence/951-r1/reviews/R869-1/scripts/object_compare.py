#!/usr/bin/env python3
"""Reviewer check: srp_mbx.c compiled for the split hart (RV32IM, the gate's SPLIT_RV32_FLAGS) at base and head.

Usage: python3 -B object_compare.py <head-repo-root> <base-ctrl-tree> <work-dir>

<base-ctrl-tree> is the base commit's sw/firmware/ctrl, extracted with git archive. For each shape (1x1/1if,
8x8/1if, 1x1/2if, 8x8/2if) both trees' srp_mbx.c are compiled with the same flags, includes and lwSRP, then
`objdump -d --no-show-raw-insn` is diffed; the differing lines are printed with the per-function sizes that
change. Nothing in either tree is written.
"""
from __future__ import annotations

import difflib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
WORK = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))

import fw_rv32  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_build import CTRL, SPLIT_RV32_FLAGS, Tree  # noqa: E402

SHAPES = (("1x1-1if", 1, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"),
          ("8x8-1if", 1, ROOT / "configs/endstation_ax7101_8x8.yaml"),
          ("1x1-2if", 2, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml"),
          ("8x8-2if", 2, ROOT / "configs/endstation_ax7101_8x8.yaml"))


def build(label: str, src: Path, interfaces: int, config: Path) -> Path:
    out = WORK / label
    tree = Tree(src, out / "build", out / "reuse")
    variant, inc = srp_arms.prepared(tree, interfaces, out, config)
    cc = fw_rv32.compiler()
    lw = ROOT / "third_party/lwSRP/src"
    obj = out / "srp_mbx.o"
    argv = [cc, *SPLIT_RV32_FLAGS, *fw_rv32.includes(cc), *inc, "-DLWSRP_MILAN=1", f"-I{lw / 'include'}", f"-I{lw}",
            "-c", str(src / "srp/srp_mbx.c"), "-o", str(obj)]
    res = subprocess.run(argv, capture_output=True, text=True)
    if res.returncode:
        raise SystemExit(f"{label}: compile failed\n{res.stderr}")
    return obj


def listing(obj: Path) -> list[str]:
    tool = fw_rv32.compiler().removesuffix("gcc") + "objdump"
    text = subprocess.run([tool, "-d", "--no-show-raw-insn", str(obj)], capture_output=True, text=True).stdout
    # drop the file name line and instruction addresses, keep the function labels and the instruction text
    lines = []
    for line in text.splitlines()[2:]:
        m = re.match(r"\s*[0-9a-f]+:\s+(.*)", line)
        text_line = m.group(1).split("#")[0].rstrip() if m else line.strip()
        # name every branch/jump target and label by its symbol, not its offset in the section
        text_line = re.sub(r"\b[0-9a-f]+ (<[^>]+>)", r"\1", text_line)
        lines.append(text_line)
    return lines


def sizes(obj: Path) -> dict[str, int]:
    tool = fw_rv32.compiler().removesuffix("gcc") + "nm"
    text = subprocess.run([tool, "-S", "--size-sort", str(obj)], capture_output=True, text=True).stdout
    return {p[3]: int(p[1], 16) for p in (ln.split() for ln in text.splitlines()) if len(p) == 4}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    print(f"compiler: {fw_rv32.compiler()}  flags: {' '.join(SPLIT_RV32_FLAGS)}")
    for name, interfaces, config in SHAPES:
        base = build(f"base-{name}", BASE, interfaces, config)
        head = build(f"head-{name}", CTRL, interfaces, config)
        a, b = listing(base), listing(head)
        diff = [d for d in difflib.unified_diff(a, b, lineterm="", n=0) if d[:1] in "+-" and d[:3] not in ("+++", "---")]
        sa, sb = sizes(base), sizes(head)
        moved = {k: (sa.get(k), sb.get(k)) for k in set(sa) | set(sb) if sa.get(k) != sb.get(k)}
        print(f"== {name}: base {len(a)} lines, head {len(b)} lines, {len(diff)} differing")
        for d in diff:
            print(f"   {d}")
        print(f"   sized symbols that differ: {moved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
