#!/usr/bin/env python3
"""Removed-check mutants for PR #612 gate 36a/36b (round 2).
Usage: mutants.py <checkout> <scratch>

Each mutant applies one or more exact, uniquely matching text edits to real-copy
files in a fresh symlink farm, runs only the focused gate 36a/36b runner (all six
gate-36 functions), and records rc plus the last error line.
KILLED = runner rc != 0.  Nothing in <checkout> is written.  8 parallel jobs.
"""
import subprocess, sys, os, pathlib
from concurrent.futures import ThreadPoolExecutor
src, scratch = map(os.path.abspath, sys.argv[1:3])
here = pathlib.Path(__file__).resolve().parent
C = "sw/builder/aem_image_checks.py"
B = "sw/builder/endstation_builder.py"
S = "sw/litex/milan_soc.py"
U = "protocol-processor/hdl/aecp/ucode/gen_ucode.py"
F = "    if False:\n"
M = [
 # named L10 refusals
 ("L10_OFFSET removed", [(C, "    if offset != list_offset:\n", F)]),
 ("L10_EMPTY removed (F2)", [(C, "    if not count:\n        raise ImageCheckError(f\"L10_EMPTY", "    if False:\n        raise ImageCheckError(f\"L10_EMPTY")]),
 ("L10_COUNT removed", [(C, "    if count > walk_count:\n", F)]),
 ("L10_PARTIAL_WORD removed", [(C, "    if partial_bytes:\n", F)]),
 ("L10_COUNT_EXTENT removed", [(C, "    elif extent_words < count:\n", "    elif False:\n")]),
 ("L10_EXTRA_WORDS removed", [(C, "    elif extent_words > count:\n", "    elif False:\n")]),
 ("L10_CURRENT removed", [(C, "    if current not in rates:\n", F)]),
 ("L10_CURRENT compares with pull bits masked", [
     (C, "    current = struct.unpack_from(\">I\", data, 136)[0]\n", "    current = struct.unpack_from(\">I\", data, 136)[0] & 0x1FFFFFFF\n"),
     (C, "    rates = struct.unpack_from(f\">{count}I\", data, offset)\n", "    rates = [r & 0x1FFFFFFF for r in struct.unpack_from(f\">{count}I\", data, offset)]\n")]),
 ("L10_HEADER removed", [(C, "        raise ImageCheckError(f\"L10_HEADER", "        pass  # (f\"L10_HEADER")]),
 # named L6 refusals
 ("L6_OFFSET removed", [(C, "    if offset != fields_end:", "    if False:")]),
 ("L6_OFFSET relaxed to round-1 lower bound", [(C, "    if offset != fields_end:", "    if offset < fields_end:")]),
 ("L6_EMPTY removed", [(C, "    if not count:\n        raise ImageCheckError(f\"L6_EMPTY", "    if False:\n        raise ImageCheckError(f\"L6_EMPTY")]),
 ("L6_EXTENT removed", [(C, "    if list_end > len(data):\n", F)]),
 ("L6_DUPLICATE removed", [(C, "    if len(set(sources)) != count:\n", F)]),
 ("L6_GAP removed", [(C, "    elif sorted(sources) != identity:\n", "    elif False:\n")]),
 ("L6_ORDER removed", [(C, "    elif sources != identity:\n", "    elif False:\n")]),
 ("L6_HEADER removed", [(C, "        raise ImageCheckError(f\"L6_HEADER", "        pass  # (f\"L6_HEADER")]),
 # presence / header (taken suggestion)
 ("L10_MISSING removed", [(C, "            if 0x0002 not in types:\n", "            if False:\n")]),
 ("L6_MISSING removed", [(C, "            if 0x0024 not in types:\n", "            if False:\n")]),
 ("zero-count rows satisfy presence", [
     (C, "            for index in range(count):\n", "            checked[cfg].add(dtype)\n            for index in range(count):\n"),
     (C, "                checked[cfg].add(dtype)\n", "")]),
 ("IMAGE_CONFIGS removed", [(C, "        if not config_count:\n", "        if False:\n")]),
 ("configuration-outside-header refusal removed", [(C, "            if cfg >= config_count:\n", "            if False:\n")]),
 # emitter hooks (F1)
 ("builder hook removed", [(B, "        aem_image_checks.validate_shipping_image(blob)\n", "        pass\n")]),
 ("SoC hook removed", [(S, "        aem_image_checks.validate_shipping_image(blob)\n", "        pass\n")]),
 ("SoC refusal swallowed", [(S, "        raise RuntimeError(f\"aem_desc.bin: {exc}\") from exc\n", "        pass\n")]),
 # index walk
 ("only index 0 of each run checked", [(C, "            for index in range(count):\n", "            for index in range(min(count, 1)):\n")]),
 ("only configuration 0 checked", [(C, "            if dtype not in (0x0002, 0x0024):", "            if cfg != 0 or dtype not in (0x0002, 0x0024):")]),
 ("CLOCK_DOMAIN rows skipped", [(C, "            if dtype not in (0x0002, 0x0024):", "            if dtype not in (0x0002,):")]),
 ("padded stride used as length", [(C, "                data = blob[start:start + length]\n                if len(data) != length:", "                data = blob[start:start + stride]\n                if len(data) != stride:")]),
 # consumer derivation
 ("consumer walk bound 9", [(U, "SSR_WALK_MAX = 8 ", "SSR_WALK_MAX = 10")]),
 ("consumer list offset 148", [(U, "SSR_LIST_OFF = 144 ", "SSR_LIST_OFF = 148 ")]),
]
def run(i, name, edits):
    farm = os.path.join(scratch, f"mut{i:02d}")
    subprocess.run(["sh", str(here / "make_farm.sh"), src, farm], check=True)
    for rel, old, new in edits:
        p = pathlib.Path(farm, rel); text = p.read_text()
        assert text.count(old) == 1, (name, rel, text.count(old))
        p.write_text(text.replace(old, new))
    r = subprocess.run([sys.executable, str(here / "run_gate36b.py"), farm],
                       capture_output=True, text=True, timeout=1800,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    out = (r.stdout + r.stderr).strip().splitlines()
    why = next((l for l in reversed(out) if "Error" in l), out[-1] if out else "")
    verdict = "KILLED" if r.returncode else "SURVIVED"
    return f"{verdict}\t{name}\trc={r.returncode}\t{why.strip()[:220]}"
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda a: run(a[0], *a[1]), enumerate(M)))
for line in res: print(line)
print(f"SUMMARY killed={sum(x.startswith('KILLED') for x in res)} of {len(res)}")
