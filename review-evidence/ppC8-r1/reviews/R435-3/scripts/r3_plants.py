#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-3 reviewer plants on the round-3 code (reviewer-owned).

usage: r3_plants.py TREE WORK [--jobs N]

Each plant is one textual replacement in an isolated copy of TREE (under
WORK); the packer gate tb/desc_store/test_gen_desc_image.py runs on the copy
and must fail (KILLED). Covers the round-3 delta: every arm of L4
stream-layout's Table 7-8 / Annex C acceptance, the R <= 8 bound, the 2R tail
length, and the shared loader with its None-spec guard. TREE is never written.
The runner is the round-2 one (r2_plants.py), unchanged.
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = "hdl/aecp/desc/model_rules.py"
L = "hdl/aecp/desc/model_lint.py"
G = "hdl/aecp/desc/gen_desc_image.py"
PLANTS = [
    ("c-offset-138-only", R, "    annex_c = offset == ANNEX_C_OFFSET\n", "    annex_c = False\n",
     "Annex C never recognised (round-2 behaviour)"),
    ("c-offset-any", R, "    if offset is not None and offset not in (FORMATS_OFFSET, ANNEX_C_OFFSET):",
     "    if False:", "moved list accepted"),
    ("c-annex-end-138", R, "    formats_end = (ANNEX_C_OFFSET if annex_c else FORMATS_OFFSET) + 8 * count",
     "    formats_end = FORMATS_OFFSET + 8 * count", "Annex C redundant_offset/length taken from Table 7-8"),
    ("c-redoff-any", R, "    if redundant is not None and redundant != formats_end:", "    if False:",
     "redundant_offset unchecked"),
    ("c-tail-in-78", R, "    if tail and not annex_c:", "    if False:", "Table 7-8 tail accepted"),
    ("c-tail-in-c-refused", R, "    if tail and not annex_c:", "    if tail:",
     "every tail refused (Annex C pair refused)"),
    ("c-rmax-any", R, "    if tail > REDUNDANT_MAX:", "    if False:", "R above 8 accepted"),
    ("c-rmax-9", R, "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 9 ", "R cap one too loose"),
    ("c-rmax-7", R, "REDUNDANT_MAX = 8 ", "REDUNDANT_MAX = 7 ", "R cap one too strict"),
    ("c-rmax-ge", R, "    if tail > REDUNDANT_MAX:", "    if tail >= REDUNDANT_MAX:", "R = 8 refused"),
    ("c-tail-8r", R, "    end = formats_end + 2 * tail", "    end = formats_end + 8 * tail",
     "tail length 8R (the assignment's reading)"),
    ("c-tail-0", R, "    end = formats_end + 2 * tail", "    end = formats_end",
     "tail length ignored"),
    ("c-length-any", R, "    if len(body) != end:\n        ctx.bad(\"stream-layout\", where, f\"is {len(body)} bytes; {made}",
     "    if len(body) < end:\n        ctx.bad(\"stream-layout\", where, f\"is {len(body)} bytes; {made}",
     "a longer stream accepted"),
    ("c-annex-136-is-137", R, "ANNEX_C_OFFSET = 136 ", "ANNEX_C_OFFSET = 137 ", "Annex C offset wrong"),
    ("g-no-guard", G, "    if spec is None or spec.loader is None:\n        raise ImportError(f\"no {name}.py beside {__file__}\")\n",
     "", "loader None-spec guard dropped"),
    ("g-own-loader", L, "model_rules = beside(\"model_rules\")",
     "import importlib.util as _u, pathlib as _p\n_s = _u.spec_from_file_location(\"model_rules\", _p.Path(__file__).with_name(\"model_rules.py\"))\nmodel_rules = _u.module_from_spec(_s); _s.loader.exec_module(model_rules)",
     "model_lint loads model_rules with its own unguarded loader again"),
]


def run(tree: Path, work: Path, plant) -> str:
    name, rel, old, new, what = plant
    copy = work / name
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy, ignore=shutil.ignore_patterns("obj_dir", "*.bin", "*.map", "__pycache__"))
    target = copy / rel
    text = target.read_text(encoding="utf-8")
    hits = text.count(old)
    if hits != 1:
        shutil.rmtree(copy)
        return f"{name} INVALID (pattern occurs {hits} times) | {what}"
    target.write_text(text.replace(old, new), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=copy / "tb/desc_store",
                          capture_output=True, text=True, timeout=600)
    tail = " ".join((proc.stdout + proc.stderr).strip().splitlines()[-3:])
    shutil.rmtree(copy)
    verdict = "KILLED" if proc.returncode != 0 else "SURVIVED"
    return f"{name} {verdict} rc={proc.returncode} {tail} | {what}"


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        lines = list(pool.map(lambda p: run(tree, work, p), PLANTS))
    print("\n".join(lines))
    killed = sum(" KILLED " in ln for ln in lines)
    print(f"{killed} of {len(lines)} KILLED; "
          f"{sum(' SURVIVED ' in ln for ln in lines)} SURVIVED; {sum(' INVALID ' in ln for ln in lines)} INVALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
