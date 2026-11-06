#!/usr/bin/env python3
"""mutants.py SOURCE_CHECKOUT WORK: one literal defect per copy, the self-test's plat checks run on each, in parallel.

CAUGHT means plat_cases raised; ESCAPED means all seven checks stayed green with the defect planted.
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SOURCE, WORK = Path(sys.argv[1]), Path(sys.argv[2])
IMAGE = "sw/firmware/ctrl/test/ctrl_plat_image.py"
CALL = "        refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n"
MUTANTS = {
    "is-file-to-exists": [(IMAGE, ".is_file()]", ".exists()]")],
    "partial-only-with-archives": [(IMAGE, "    if flash_map is not None:\n",
                                    "    if flash_map is not None and any(path.exists() for path in archives):\n")],
    "refusal-after-generators": [(IMAGE, CALL, ""),
                                 (IMAGE, "    objects = []\n    for index, src in enumerate(sources):\n",
                                  "    refuse_placeholder(args.flash_map, (args.libc, args.compiler_runtime))\n"
                                  "    objects = []\n    for index, src in enumerate(sources):\n")],
    "headers-reversed": [(IMAGE, 'MAP_HEADERS = ("generated/csr.h", "generated/mem.h")',
                          'MAP_HEADERS = ("generated/mem.h", "generated/csr.h")')],
    "header-refusal-removed": [(IMAGE, "        if missing:\n", "        if False:\n")],
    "mem-not-required": [(IMAGE, 'MAP_HEADERS = ("generated/csr.h", "generated/mem.h")',
                          'MAP_HEADERS = ("generated/csr.h",)')],
    "refused-only-when-both-missing": [(IMAGE, "        if missing:\n", "        if len(missing) == 2:\n")],
    "refused-only-when-one-missing": [(IMAGE, "        if missing:\n", "        if len(missing) == 1:\n")],
}
DRIVER = ("import sys; sys.path.insert(0, 'sw/firmware/ctrl/test'); from pathlib import Path; "
          "import ctrl_image_selftest as t; print('plat checks', t.plat_cases(Path(sys.argv[1])))")


def one(item):
    """Plant one mutant in its own copy and run the plat checks there."""
    name, edits = item
    tree = WORK / name
    shutil.copytree(SOURCE, tree, symlinks=True)
    for path, old, new in edits:
        target = tree / path
        text = target.read_text()
        assert text.count(old) == 1, (name, old)
        target.write_text(text.replace(old, new))
    done = subprocess.run([sys.executable, "-B", "-c", DRIVER, str(WORK / f"{name}-out")], cwd=tree,
                          capture_output=True, text=True, check=False)
    said = (done.stdout + done.stderr).strip().splitlines()
    passed = sum(line.startswith("PASS: plat") for line in said)
    verdict = "ESCAPED" if done.returncode == 0 else "CAUGHT"
    return f"{name}: {verdict}, rc {done.returncode}, {passed} plat checks passed first: {said[-1][:170] if said else ''}"


with ThreadPoolExecutor(8) as pool:
    results = list(pool.map(one, MUTANTS.items()))
print("\n".join(results))
print(f"mutants: {len(results)} planted, {sum('ESCAPED' in r for r in results)} escaped")
