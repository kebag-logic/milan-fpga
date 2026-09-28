#!/usr/bin/env python3
"""Removed-check and structural mutants of the #577 checker, killed or not by gate 36b.

Round 2 (head be6b48c1): adds the SoC-emitter hook, F2, offset-76, presence and
current-rate mutants; rm_L6_EXTENT follows the head expression.

usage: mutants.py <pristine-tree> <work-dir> <name>   (one mutant; prints verdict)
       mutants.py --list
Each mutant hard-links the pristine tree, replaces exactly one file with a
single textual substitution (which must match exactly once), and runs only the
committed gate 36b functions through run_gate36b.py.
"""
import subprocess, sys, shutil
from pathlib import Path

C = "sw/builder/aem_image_checks.py"
B = "sw/builder/endstation_builder.py"
U = "protocol-processor/hdl/aecp/ucode/gen_ucode.py"
S = "sw/litex/milan_soc.py"
MUTANTS = {
    # one per required refusal class (removed check), round 1
    "rm_L10_OFFSET": (C, "    if offset != list_offset:\n", "    if False:\n"),
    "rm_L10_COUNT": (C, "    if count > walk_count:\n", "    if False:\n"),
    "rm_L10_COUNT_EXTENT": (C, "    elif extent_words < count:\n", "    elif False:\n"),
    "rm_L10_PARTIAL_WORD": (C, "    if partial_bytes:\n", "    if False:\n"),
    "rm_L10_EXTRA_WORDS": (C, "    elif extent_words > count:\n", "    elif False:\n"),
    "rm_L6_ORDER": (C, "    elif sources != identity:\n", "    elif False:\n"),
    "rm_L6_GAP": (C, "    elif sorted(sources) != identity:\n", "    elif False:\n"),
    "rm_L6_DUPLICATE": (C, "    if len(set(sources)) != count:\n", "    if False:\n"),
    # defensive refusals
    "rm_L10_HEADER": (C, "    if len(data) < fields_end:\n        raise ImageCheckError(f\"L10_HEADER",
                      "    if False:\n        raise ImageCheckError(f\"L10_HEADER"),
    "rm_L6_HEADER": (C, "    if len(data) < fields_end:\n        raise ImageCheckError(f\"L6_HEADER",
                     "    if False:\n        raise ImageCheckError(f\"L6_HEADER"),
    "rm_L6_EMPTY": (C, "    if not count:\n        raise ImageCheckError(f\"L6_EMPTY",
                    "    if False:\n        raise ImageCheckError(f\"L6_EMPTY"),
    "rm_L6_EXTENT": (C, "    if list_end > len(data):\n", "    if False:\n"),
    # round 2: F2 and the taken suggestions
    "rm_L10_EMPTY": (C, "    if not count:\n        raise ImageCheckError(f\"L10_EMPTY",
                     "    if False:\n        raise ImageCheckError(f\"L10_EMPTY"),
    "rm_L10_CURRENT": (C, "    if current not in rates:\n", "    if False:\n"),
    "current_masks_pull": (C, "    if current not in rates:\n",
                           "    if current & 0x1FFFFFFF not in [r & 0x1FFFFFFF for r in rates]:\n"),
    "current_first_only": (C, "    if current not in rates:\n", "    if current != rates[0]:\n"),
    "rm_L6_OFFSET": (C, "    if offset != fields_end:  # IEEE", "    if False:  # IEEE"),
    "L6_OFFSET_relaxed_ge": (C, "    if offset != fields_end:  # IEEE", "    if offset < fields_end:  # IEEE"),
    "rm_L10_MISSING": (C, "            if 0x0002 not in types:\n", "            if False:\n"),
    "rm_L6_MISSING": (C, "            if 0x0024 not in types:\n", "            if False:\n"),
    "rm_IMAGE_CONFIGS": (C, "        if not config_count:\n", "        if False:\n"),
    "presence_counts_rows": (C, "            for index in range(count):\n                start",
                             "            checked[cfg].add(dtype) if cfg < config_count else None\n            for index in range(count):\n                start"),
    "presence_config0_only": (C, "        for cfg, types in enumerate(checked):\n", "        for cfg, types in enumerate(checked[:1]):\n"),
    "rm_cfg_range": (C, "            if cfg >= config_count:\n", "            if False:\n"),
    # generic structure refusals (outside the frozen classes; informational)
    "rm_IMAGE_magic_version": (C, "        if blob[:4] != b\"AEMI\" or struct.unpack_from(\">H\", blob, 4)[0] != 1:\n", "        if False:\n"),
    "rm_IMAGE_desc_beyond": (C, "                if len(data) != length:\n", "                if False:\n"),
    # wiring / walk mutants
    "rm_builder_hook": (B, "        aem_image_checks.validate_shipping_image(blob)\n", "        pass\n"),
    "rm_soc_hook": (S, "        aem_image_checks.validate_shipping_image(blob)\n", "        pass\n"),
    "soc_hook_swallows": (S, "        raise RuntimeError(f\"aem_desc.bin: {exc}\") from exc\n",
                          "        print(f\"warning: aem_desc.bin: {exc}\")\n"),
    "soc_repack_after_check": (S, "    return blob, report, overlay\n",
        "    blob = _img.build(_join.model_to_document(model, _join.identity_from_overlay(ovl)), 576)[0]\n    return blob, report, overlay\n"),
    "walk_index0_only": (C, "            for index in range(count):\n", "            for index in range(min(count, 1)):\n"),
    "walk_len_as_stride": (C, "                start = base + index * stride\n", "                start = base + index * length\n"),
    "walk_config0_only": (C, "            if dtype not in (0x0002, 0x0024):", "            if cfg != 0 or dtype not in (0x0002, 0x0024):"),
    # control: semantically identical rewrite; must SURVIVE (no spurious kill)
    "noop_control": (C, "        for row in range(row_count):\n", "        for row in range(min(row_count, 1) if False else row_count):\n        # (control: no-op rewrite)\n"),
    "noop_control_soc": (S, "    return blob, report, overlay\n", "    blob = bytes(blob)  # control: same bytes\n    return blob, report, overlay\n"),
    "walk_first_run_per_type": (C, "            if dtype not in (0x0002, 0x0024):  # IEEE 7.2 AUDIO_UNIT / CLOCK_DOMAIN.\n                continue\n",
        "            if dtype not in (0x0002, 0x0024):  # IEEE 7.2 AUDIO_UNIT / CLOCK_DOMAIN.\n                continue\n            if (cfg, dtype) in seen:\n                continue\n            seen.add((cfg, dtype))\n"),
    "len_uses_stride": (C, "                data = blob[start:start + length]\n", "                data = blob[start:start + stride]\n"),
    # consumer drift: a test that pinned only the consumer's own values would not notice
    "consumer_offset_146": (U, "SSR_LIST_OFF = 144 ", "SSR_LIST_OFF = 146 "),
    "consumer_walk_9": (U, "SSR_WALK_MAX = 8 ", "SSR_WALK_MAX = 9 "),
}

def main():
    if sys.argv[1] == "--list":
        print("\n".join(MUTANTS)); return 0
    pristine, work, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    rel, old, new = MUTANTS[name]
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(["cp", "-al", str(pristine), str(tree)], check=True)
    target = tree / rel
    text = target.read_text()
    assert text.count(old) == 1, f"{name}: pattern matches {text.count(old)} times"
    target.unlink()  # break the hard link before writing
    out = text.replace(old, new)
    if name == "walk_first_run_per_type":
        out = out.replace("        row_count = struct.unpack_from", "        seen = set()\n        row_count = struct.unpack_from", 1)
    target.write_text(out)
    runner = Path(__file__).with_name("run_gate36b.py")
    r = subprocess.run([sys.executable, str(runner), str(tree)], capture_output=True, text=True, timeout=1200)
    (work / f"{name}.log").write_text(r.stdout + r.stderr)
    fails = [l for l in r.stdout.splitlines() if l.startswith("RESULT") and " FAIL " in l]
    verdict = "KILLED" if r.returncode else "SURVIVED"
    print(f"{name}\t{verdict}\trc={r.returncode}\t{' | '.join(fails)[:400]}")
    shutil.rmtree(tree)
    return 0

sys.exit(main())
