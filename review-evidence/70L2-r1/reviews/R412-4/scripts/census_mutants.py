#!/usr/bin/env python3
"""Apply one reviewer-defined census mutant to a DISPOSABLE tree's
sw/builder/test_builder.py.  Usage: census_mutants.py <tree> <mutant-id>

Each mutant weakens the verdict's image pins in one place; a mutant is KILLED
when test_baremetal_profile_contract() fails on it.  N0 is the null mutant
(no edit).  K7 is the first-byte-only reference range (the round-3 "target !=
low" class); K8 shrinks the pins function's own range to one byte."""
import sys
from pathlib import Path

MUTANTS = {
    "N0": [],
    "K0": [("        broken = []\n        references = rv32_image_references(image, low, high)\n",
            "        broken = []\n        references = rv32_image_references(image, low, high)\n"
            "        return [], references\n")],
    "K1": [("        if stores != [\"milan_init()\"] or \\\n",
            "        if False or \\\n")],
    "K2": [("                writes != [(\"milan_init\", Rv32Tag(\"call:load_aem_image\"))]:\n",
            "                False:\n")],
    "K3": [("        if escapes:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}",
            "        if False:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}")],
    "K4": [("        if others:\n            broken.append(f\"{VERDICT_PIN_NAME}",
            "        if False:\n            broken.append(f\"{VERDICT_PIN_NAME}")],
    "K5": [("        if not verdict[\"local\"]:\n            broken.append(VERDICT_PIN_LOCAL)",
            "        if False:\n            broken.append(VERDICT_PIN_LOCAL)")],
    "K6": [("        elif image[\"bare_auipc\"]:\n",
            "        elif False:\n")],
    "K7": [("        if target is not None and not low <= target < high:\n            continue\n",
            "        if target is not None and target != low:\n            continue\n")],
    "K8": [("        low, high = verdict[\"value\"], verdict[\"value\"] + verdict[\"size\"]\n        placed =",
            "        low, high = verdict[\"value\"], verdict[\"value\"] + 1\n        placed =")],
    # the planted break itself moved, to show its premise check can fail
    "B1": [("        \"(char *)(&milan_verdict_next - 1) + 1);\\n\",\n",
            "        \"(char *)(&milan_verdict_next - 1) + 4);\\n\",\n")],
    "B2": [("        \"(char *)(&milan_verdict_next - 1) + 1);\\n\",\n",
            "        \"(char *)(&milan_verdict_next - 1) + 0);\\n\",\n")],
}

#: Every tree also gets a stop point just after gate 1b prints its resolved
#: note (the closing line naming the verdict breaks), so one run fits the
#: session's foreground limit; the stop prints a marker.
STOP_ANCHOR = "          + resolved_note)\n"
STOP = ("          + resolved_note)\n"
        "    print('R412 STOP AFTER RESOLVED NOTE', flush=True)\n"
        "    raise SystemExit(0)\n")

tree, mid = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text(encoding="utf-8")
for old, new in MUTANTS[mid]:
    assert text.count(old) == 1, f"{mid}: anchor count {text.count(old)}: {old!r}"
    text = text.replace(old, new)
assert text.count(STOP_ANCHOR) == 1, "stop anchor"
text = text.replace(STOP_ANCHOR, STOP)
path.write_text(text, encoding="utf-8")
print(f"{mid} applied to {path}")
