#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Round-2 reviewer plants on the round-2 code (reviewer-owned).

usage: r2_plants.py TREE WORK [--jobs N]

Each plant is one textual replacement in an isolated copy of TREE (under
WORK); the packer gate tb/desc_store/test_gen_desc_image.py runs on the copy
and must fail (KILLED). Covers the round-2 arms (L12, identify-format, the
digest families, waiver typing/overlap, per-port L5, CONTROL-only L2, CRF
word) and the internal round-1 reviewer's five unpinned arms as re-expressed
on the round-2 code. TREE is never written.
"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = "hdl/aecp/desc/model_rules.py"
L = "hdl/aecp/desc/model_lint.py"
PLANTS = [
    # name, file, old, new, what it weakens
    ("l12-max-509", R, "DESCRIPTOR_MAX = 508", "DESCRIPTOR_MAX = 509", "508 maximum one too loose"),
    ("l12-max-507", R, "DESCRIPTOR_MAX = 508", "DESCRIPTOR_MAX = 507", "508 maximum one too strict"),
    ("l12-no-fixed", R, "        if len(body) != size:\n            ctx.bad(\"descriptor-extent\"",
     "        if len(body) < size:\n            ctx.bad(\"descriptor-extent\"", "fixed extent: longer accepted"),
    ("l12-no-offset", R, "    if offset is not None and offset != size:", "    if False:", "variable offset arm dropped"),
    ("l12-cluster-91", R, "D.AUDIO_CLUSTER: (90, None)", "D.AUDIO_CLUSTER: (91, None)", "AUDIO_CLUSTER extent wrong"),
    ("l12-entity-gone", R, "    D.ENTITY: (312, None), ", "    ", "ENTITY extent dropped"),
    ("l12-map-gone", R, ", D.AUDIO_MAP: (8, (4, 6, 8))", "", "AUDIO_MAP extent dropped"),
    ("id-no-length", R, "    wrong = [f\"is {len(body)} bytes, not 113\"] if len(body) != 113 else []",
     "    wrong = []", "IDENTIFY 113-octet length unchecked"),
    ("id-step-any", R, "(106, 1, 255, \"step\"), ", "", "IDENTIFY step unchecked"),
    ("id-unit-any", R, ", (109, 2, 0x0000, \"unit\")", "", "IDENTIFY unit unchecked"),
    ("id-nvalues-any", R, "(96, 2, 1, \"number_of_values\"),", "", "IDENTIFY number_of_values unchecked"),
    ("id-type-any", R, "IDENTIFY_FORMAT = ((80, 2, 0x0001, \"control_value_type\"), ", "IDENTIFY_FORMAT = (", "IDENTIFY value type unchecked"),
    ("id-offset-any", R, "(94, 2, 104, \"values_offset\"),", "", "IDENTIFY values_offset unchecked"),
    ("id-min-any", R, "(104, 1, 0, \"minimum\"),", "", "IDENTIFY minimum unchecked"),
    ("id-max-any", R, "(105, 1, 255, \"maximum\"), ", "", "IDENTIFY maximum unchecked (the pinned arm)"),
    ("id-no-mask", R, "                found &= 0x3FFF", "                pass", "IDENTIFY value_type flag bits not masked"),
    ("dig-selector-whole", L, "    if family == \"selector\":\n        return [(offset, offset + width)]",
     "    if family == \"selector\":\n        return [(offset, 10**6)]", "selector: whole value_details excluded"),
    ("dig-array-off", L, "        return [(offset + 4 + 4 * width, offset + 4 + (4 + count) * width)]",
     "        return [(offset + 4 * width, offset + 4 + (4 + count) * width)]", "array exclusion starts at unit"),
    ("dig-linear-step", L, "        step = 5 * width + 4", "        step = 5 * width", "linear entry stride wrong"),
    ("dig-int8", L, "        if base + 1 <= value_type <= base + 9:", "        if base <= value_type <= base + 9:",
     "INT8 types excluded (beyond the clause)"),
    ("dig-mixer-all", L, "D.MIXER: (80, 86, None, frozenset({\"linear\"}))",
     "D.MIXER: (80, 86, None, frozenset({\"linear\", \"selector\", \"array\"}))", "MIXER families widened"),
    ("dig-named-1e", L, "| frozenset(range(0x1F, 0x29))", "| frozenset(range(0x1E, 0x29))",
     "MATRIX_SIGNAL bytes 4..67 zeroed again"),
    ("dig-avb-port", L, "D.AVB_INTERFACE: ((70, 76), (78, 96)),", "D.AVB_INTERFACE: ((70, 76), (78, 98)),",
     "AVB_INTERFACE port_number excluded"),
    ("dig-cs-loc", L, "D.CLOCK_SOURCE: ((70, 72), (74, 82)),", "D.CLOCK_SOURCE: ((70, 72), (74, 86)),",
     "CLOCK_SOURCE location excluded"),
    ("dig-entity-caps", L, "D.ENTITY: ((4, 20), (36, 112)", "D.ENTITY: ((4, 24), (36, 112)",
     "entity_capabilities excluded"),
    ("w-type-coerce", L, "    if isinstance(item[\"type\"], bool) or not isinstance(item[\"type\"], (str, int)):",
     "    if False:", "waiver type not type-checked"),
    ("w-int-coerce", L, "        if key in item and (isinstance(item[key], bool) or not isinstance(item[key], int)):",
     "        if False:", "waiver integers not type-checked"),
    ("w-overlap-off", L, "        if other is None:\n            parsed.append(waiver)",
     "        if True:\n            parsed.append(waiver)", "overlapping waivers accepted"),
    ("w-overlap-cfg", L, "        if (other.check, other.where[:2]) == (waiver.check, waiver.where[:2]) \\",
     "        if (other.check, other.where[1]) == (waiver.check, waiver.where[1]) \\",
     "overlap ignores configuration"),
    ("l5-any-move", R, "            if seen[1] != index:", "            if False:", "per-port move accepted"),
    ("l2-no-range", R, "            if base < end:", "            if False:", "L2 range arm dropped"),
    ("l2-no-top", R, "        if top and walked and max(top) > min(walked):", "        if False:",
     "L2 configuration-first arm dropped"),
    ("crf-any-word", R, "                other = sorted({w for w in words if _family(w) == \"CRF\" and w != CRF_MILAN})",
     "                other = [] if CRF_MILAN in words else sorted({w for w in words if _family(w) == \"CRF\"})",
     "round-1 CRF check (Milan word present suffices)"),
    ("owners-no-jack", R, "CONTROL_OWNERS = ((D.JACK_INPUT, 74, 76), (D.JACK_OUTPUT, 74, 76), ",
     "CONTROL_OWNERS = (", "JACK CONTROLs counted top-level again"),
    ("unique-per-map", R, "        seen: dict[tuple[int, int], int] = {}\n        for index in sorted(ctx.of(cfg, D.AUDIO_MAP)):",
     "        for index in sorted(ctx.of(cfg, D.AUDIO_MAP)):\n            seen: dict[tuple[int, int], int] = {}",
     "uniqueness reset per AUDIO_MAP"),
    ("layout-no-length", R, "    if len(body) != end:\n        ctx.bad(\"stream-layout\"",
     "    if False:\n        ctx.bad(\"stream-layout\"", "stream body-length arm dropped"),
    ("stale-cfg", L, "            if cfg not in ctx.model:\n                problems.append",
     "            if False:\n                problems.append", "waiver on a missing configuration not stale"),
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
