#!/usr/bin/env python3
"""Removed-check mutants for PR #612 gate 36b.  Usage: mutants.py <checkout> <scratch>

Each mutant edits one real-copy file in a fresh symlink farm, runs only the
focused gate 36a/36b runner, and records rc plus the first failure line.
KILLED = runner rc != 0.  Nothing in <checkout> is written.
"""
import subprocess, sys, os, pathlib
src, scratch = map(os.path.abspath, sys.argv[1:3])
here = pathlib.Path(__file__).resolve().parent
C = "sw/builder/aem_image_checks.py"
B = "sw/builder/endstation_builder.py"
U = "protocol-processor/hdl/aecp/ucode/gen_ucode.py"
M = [
 ("L10_OFFSET removed", C, "    if offset != list_offset:\n", "    if False:\n"),
 ("L10_COUNT removed", C, "    if count > walk_count:\n", "    if False:\n"),
 ("L10_PARTIAL_WORD removed", C, "    if partial_bytes:\n", "    if False:\n"),
 ("L10_COUNT_EXTENT removed", C, "    elif extent_words < count:\n", "    elif False:\n"),
 ("L10_EXTRA_WORDS removed", C, "    elif extent_words > count:\n", "    elif False:\n"),
 ("L6_DUPLICATE removed", C, "    if len(set(sources)) != count:\n", "    if False:\n"),
 ("L6_GAP removed", C, "    elif sorted(sources) != identity:\n", "    elif False:\n"),
 ("L6_ORDER removed", C, "    elif sources != identity:\n", "    elif False:\n"),
 ("L6_EMPTY removed", C, "    if not count:\n", "    if False:\n"),
 ("L6_EXTENT removed", C, "    if offset < fields_end or list_end > len(data):\n", "    if False:\n"),
 ("L10_HEADER removed", C, "        raise ImageCheckError(f\"L10_HEADER", "        pass  # (f\"L10_HEADER"),
 ("L6_HEADER removed", C, "        raise ImageCheckError(f\"L6_HEADER", "        pass  # (f\"L6_HEADER"),
 ("builder hook removed", B, "        aem_image_checks.validate_shipping_image(blob)\n", "        pass\n"),
 ("only index 0 of each run checked", C, "            for index in range(count):\n", "            for index in range(min(count, 1)):\n"),
 ("only configuration 0 checked", C, "            if dtype not in (0x0002, 0x0024):", "            if cfg != 0 or dtype not in (0x0002, 0x0024):"),
 ("CLOCK_DOMAIN rows skipped", C, "            if dtype not in (0x0002, 0x0024):", "            if dtype not in (0x0002,):"),
 ("padded stride used as length", C, "                data = blob[start:start + length]\n                if len(data) != length:", "                data = blob[start:start + stride]\n                if len(data) != stride:"),
 ("consumer walk bound 9", U, "SSR_WALK_MAX = 8 ", "SSR_WALK_MAX = 10"),
 ("consumer list offset 148", U, "SSR_LIST_OFF = 144 ", "SSR_LIST_OFF = 148 "),
]
res = []
for i, (name, rel, old, new) in enumerate(M):
    farm = os.path.join(scratch, f"mut{i:02d}")
    subprocess.run(["sh", str(here / "make_farm.sh"), src, farm], check=True)
    p = pathlib.Path(farm, rel)
    text = p.read_text()
    assert text.count(old) == 1, (name, text.count(old))
    p.write_text(text.replace(old, new))
    r = subprocess.run([sys.executable, str(here / "run_gate36b.py"), farm],
                       capture_output=True, text=True, timeout=1200)
    out = (r.stdout + r.stderr).strip().splitlines()
    why = next((l for l in reversed(out) if "Error" in l), out[-1] if out else "")
    verdict = "KILLED" if r.returncode else "SURVIVED"
    res.append(f"{verdict}\t{name}\trc={r.returncode}\t{why.strip()[:200]}")
    print(res[-1], flush=True)
print(f"SUMMARY killed={sum(x.startswith('KILLED') for x in res)} of {len(res)}")
