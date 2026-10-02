#!/usr/bin/env python3
"""Round-3 boundary plants on the new L4 stream-layout code: one textual
replacement per disposable copy of TREE; the packer gate must fail on each.
usage: f1_plants.py TREE WORK"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = "hdl/aecp/desc/model_rules.py"
PLANTS = (
    ("annex-c-refused", "offset not in (FORMATS_OFFSET, ANNEX_C_OFFSET)", "offset != FORMATS_OFFSET"),
    ("annex-c-formats-at-138", "(ANNEX_C_OFFSET if annex_c else FORMATS_OFFSET)", "FORMATS_OFFSET"),
    ("redundant-max-7", "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 7 "),
    ("redundant-max-9", "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 9 "),
    ("tail-not-in-length", "    end = formats_end + 2 * tail\n", "    end = formats_end\n"),
    ("tail-8-octets", "    end = formats_end + 2 * tail\n", "    end = formats_end + 8 * tail\n"),
    ("table-7-8-tail-accepted", "    if tail and not annex_c:\n", "    if False:\n"),
    ("annex-c-tail-refused", "    if tail and not annex_c:\n", "    if tail:\n"),
    ("annex-c-offset-137", "ANNEX_C_OFFSET = 136 ", "ANNEX_C_OFFSET = 137 "),
)


def run(tree: Path, work: Path, plant: tuple[str, str, str]) -> str:
    name, old, new = plant
    copy = work / name
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(tree / "hdl/aecp/desc", copy / "hdl/aecp/desc")
    shutil.copytree(tree / "tb/desc_store", copy / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
    text = (copy / R).read_text(encoding="utf-8")
    if text.count(old) != 1:
        return f"{name} BADPLANT ({text.count(old)})"
    (copy / R).write_text(text.replace(old, new), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=copy / "tb/desc_store",
                          capture_output=True, text=True, timeout=600)
    fails = sorted({ln.split(" (")[0] for ln in proc.stderr.splitlines() if ln.startswith(("FAIL:", "ERROR:"))})
    shutil.rmtree(copy)
    return f"{name} {'KILLED' if proc.returncode else 'SURVIVED'} {fails[:3]}"


if __name__ == "__main__":
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    with ThreadPoolExecutor(max_workers=9) as pool:
        lines = list(pool.map(lambda p: run(tree, work, p), PLANTS))
    print("\n".join(lines))
    print(f"{sum(' KILLED ' in ln for ln in lines)} of {len(lines)} KILLED")
