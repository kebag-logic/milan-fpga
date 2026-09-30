#!/usr/bin/env python3
"""Plant one mutant of gate 1b's linked-image census into a tree copy.

usage: census_mutants.py <tree> <mutant>

Each mutant weakens one pin of verdict_image_pins() / rv32_image_references()
at the exact head; the WHOLE gate 1b is then run on the unplanted shipping
firmware, and a mutant is KILLED when gate 1b fails (one of its own planted
pin-break controls is accepted, or refused without naming its pins).

  M1_no_escape      the escape pin never breaks
  M2_no_name        the one-name pin never breaks
  M3_no_local       the locality pin never breaks
  M4_no_auipc       the AUIPC pin never breaks
  M5_no_image_store the store pin's IMAGE half (in-place stores) is dropped
  M6_no_resolver_store the store pin's RESOLVER half is dropped
  M7_addi_in_place  `%lo` on an OP-IMM (addi) is read as a load in place
  M8_no_image       verdict_image_pins() breaks nothing and sees nothing
  M9_by_name_only   only relocations whose target is EXACTLY the verdict's
                    first byte are references (a narrower address test)
"""
import sys
from pathlib import Path

tree, kind = Path(sys.argv[1]), sys.argv[2]
path = tree / "sw/builder/test_builder.py"
text = path.read_text()

MUTANTS = {
    "M1_no_escape": ("        if escapes:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}",
                     "        if False:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}"),
    "M2_no_name": ("        if others:\n            broken.append(f\"{VERDICT_PIN_NAME}",
                   "        if False:\n            broken.append(f\"{VERDICT_PIN_NAME}"),
    "M3_no_local": ("        if not verdict[\"local\"]:\n            broken.append(VERDICT_PIN_LOCAL)",
                    "        if False:\n            broken.append(VERDICT_PIN_LOCAL)"),
    "M4_no_auipc": ("        elif image[\"bare_auipc\"]:\n",
                    "        elif False:\n"),
    "M5_no_image_store": ("        if stores != [\"milan_init()\"] or \\\n",
                          "        if False or \\\n"),
    "M6_no_resolver_store": ("                writes != [(\"milan_init\", Rv32Tag(\"call:load_aem_image\"))]:\n",
                             "                False:\n"),
    "M7_addi_in_place": ("                and opcode in RV32_OPCODE_LOADS:\n",
                         "                and opcode in RV32_OPCODE_LOADS | {RV32_OPCODE_OP_IMM}:\n"),
    "M8_no_image": ("        broken, references = verdict_image_pins(image, unit)\n",
                    "        broken, references = [], []\n"),
    "M9_by_name_only": ("        if target is not None and not low <= target < high:\n",
                        "        if target is not None and target != low:\n"),
}
old, new = MUTANTS[kind]
assert text.count(old) == 1, (kind, text.count(old))
path.write_text(text.replace(old, new, 1))
print(f"mutated {kind} in {path}")
