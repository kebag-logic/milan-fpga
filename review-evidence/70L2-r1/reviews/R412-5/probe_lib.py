#!/usr/bin/env python3
"""R412-5 probe harness for PR #623 gate 1b (portable, disposable trees only).

make_variant(name, edits) copies the pristine scratch base tree to
scratch/v/<name> and applies exact, count-checked text edits to
sw/builder/test_builder.py (or another file), always adding the observation
hook below. The hook never changes a verdict: it only prints, and in stop mode
ends the run with rc 0 right after gate 1b's verdict controls.

Usage: probe_lib.py <variant-name>   (variants are defined in VARIANTS)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / "scratch"
BASE = SCRATCH / "base"
TB = "sw/builder/test_builder.py"

# ---- observation hook (prints only; stop mode exits after verdict controls)
HOOK_ANCHOR = ("    #: ... and the store-class mutants measured on the "
               "resolver ALONE, so\n")
HOOK = (
    "    if __import__('os').environ.get('R412_STOP'):\n"
    "        print('R412 STOP ran=%s kept=%s refused=%d/%d interior_bytes=%s'"
    " % (baseline_census_verdict['ran'],"
    " accepted.get('kept') if baseline_census_verdict['ran'] else None,"
    " len(verdict_pin_refused), len(verdict_pin_breaks),"
    " verdict_interior_bytes), flush=True)\n"
    "        raise SystemExit(0)\n")
REFUSAL_ANCHOR = "                verdict_pin_refused.append(what)\n"
REFUSAL_HOOK = (
    "                print('R412 REFUSED %s :: pins named: %s' % (what, [n for"
    " n, p in (('write', VERDICT_PIN_WRITE), ('escape', VERDICT_PIN_ESCAPE),"
    " ('name', VERDICT_PIN_NAME), ('local', VERDICT_PIN_LOCAL),"
    " ('pcrel', VERDICT_PIN_PCREL), ('address', VERDICT_PIN_ADDRESS),"
    " ('static', VERDICT_PIN_STATIC), ('unit', VERDICT_PIN_UNIT))"
    " if p in str(exc)]), flush=True)\n")
PREMISE_ANCHOR = "            verdict_interior_bytes.extend(reached)\n"
PREMISE_HOOK = ("            print('R412 PREMISE +%d reached %s' % (offset, "
                "reached), flush=True)\n")


def edit(text, old, new, count=1, label=""):
    found = text.count(old)
    if found != count:
        raise SystemExit(f"EDIT ANCHOR {label!r}: found {found}, want {count}")
    return text.replace(old, new)


def hooked(text):
    text = edit(text, HOOK_ANCHOR, HOOK + HOOK_ANCHOR, label="stop hook")
    text = edit(text, REFUSAL_ANCHOR, REFUSAL_ANCHOR + REFUSAL_HOOK,
                label="refusal hook")
    return edit(text, PREMISE_ANCHOR, PREMISE_ANCHOR + PREMISE_HOOK,
                label="premise hook")


# ---- census narrowings (my own; not copied from any earlier packet)
REF_FILTER = "        if target is not None and not low <= target < high:\n"
def drop_ref_byte(k):
    """rv32_image_references() stops reading byte +k of the range."""
    return [(TB, REF_FILTER,
             "        if target is not None and (not low <= target < high or "
             f"target == low + {k}):\n")]
def ref_prefix(n):
    """rv32_image_references() reads only the first n bytes."""
    return [(TB, REF_FILTER,
             "        if target is not None and not low <= target < "
             f"min(high, low + {n}):\n")]
PIN_RANGE = ('        low, high = verdict["value"], verdict["value"] + '
             'verdict["size"]\n')
def pin_prefix(n):
    """verdict_image_pins() takes the verdict to be n bytes long."""
    return [(TB, PIN_RANGE,
             f'        low, high = verdict["value"], verdict["value"] + {n}\n')]
def pin_suffix(n):
    """verdict_image_pins() starts the verdict n bytes in (drops the head)."""
    return [(TB, PIN_RANGE,
             f'        low, high = verdict["value"] + {n}, verdict["value"] + '
             'verdict["size"]\n')]
ROLE_ESC = ("        elif kind in (kinds[\"R_RISCV_LO12_I\"], "
            "kinds[\"R_RISCV_PCREL_LO12_I\"]) \\\n"
            "                and opcode == RV32_OPCODE_OP_IMM:\n"
            "            role = \"the full address formed in a register (%lo "
            "on an addi)\"\n")
def lo_addi_upper_off_start(k):
    """a %lo on an addi at byte +k is treated as an in-place upper part."""
    return [(TB, ROLE_ESC, ROLE_ESC.replace(
        "            role = \"the full address formed in a register (%lo on "
        "an addi)\"\n",
        f"            role = (RV32_ROLE_UPPER if target == low + {k} else "
        "\"the full address formed in a register (%lo on an addi)\")\n"))]

# ---- premise weakenings (the per-break check itself)
PREMISE = "            assert reached == [offset], \\\n"
def premise(expr):
    return [(TB, PREMISE, f"            assert {expr}, \\\n")]

# ---- break relocations (the planted controls themselves)
def move_break(k, new_offset):
    old = ("                       \"(char *)(&milan_verdict_next - 1) + "
           f"{k});\\n\",\n")
    new = ("                       \"(char *)(&milan_verdict_next - 1) + "
           f"{new_offset});\\n\",\n")
    return [(TB, old, new)]

VARIANTS = {
    "H0_head": [],
    # one byte dropped from the census reference reader
    "D0_drop_byte0": drop_ref_byte(0),
    "D1_drop_byte1": drop_ref_byte(1),
    "D2_drop_byte2": drop_ref_byte(2),
    "D3_drop_byte3": drop_ref_byte(3),
    # prefix narrowings of the reference reader (M9 / N1 / N2 shapes)
    "P1_ref_first1": ref_prefix(1),
    "P2_ref_first2": ref_prefix(2),
    "P3_ref_first3": ref_prefix(3),
    # the same narrowings applied to the pins' own range instead
    "R1_pin_first1": pin_prefix(1),
    "R2_pin_first2": pin_prefix(2),
    "R3_pin_first3": pin_prefix(3),
    "S1_pin_skip_head1": pin_suffix(1),
    # role mis-classification at one byte only (escape seen as upper)
    "E2_lo_addi_byte2_upper": lo_addi_upper_off_start(2),
    "E3_lo_addi_byte3_upper": lo_addi_upper_off_start(3),
    # premise weakened to round 4's form, then with a break misplaced
    "Q0_premise_r4_moved3to1": premise(
        "reached and 0 not in reached") + move_break(3, 1),
    "Q1_moved2to_neighbour": move_break(2, 6),
    "Q2_moved3to1": move_break(3, 1),
    "Q3_moved2to0": move_break(2, 0),
    "Q4_premise_membership_moved3to1": premise(
        "offset in reached") + move_break(3, 1),
}

# ---- limit-class probes planted in the SHIPPING firmware (whole gate run)
FW = "sw/firmware/milan_baremetal/milan_baremetal.c"
NVM_OPEN = "static void nvm_boot(void)\n{\n"
def plant(statement, declare=None):
    edits = [(FW, NVM_OPEN, NVM_OPEN + statement)]
    if declare:
        edits.append((FW, "static int aem_loaded;\n",
                      declare + "static int aem_loaded;\n"))
    return edits

VARIANTS.update({
    "L1_csr_pointer_sscanf": plant(
        "\t(void)sscanf(\"\\001\", \"%c\", "
        "(char *)(uintptr_t)milan_read(MILAN_ID));\n"),
    "L2_stack_runtime_sscanf": plant(
        "\t{ char loc[4]; (void)sscanf(\"\\001\", \"%c\", "
        "loc + (int)milan_read(MILAN_ID)); }\n"),
    "L3_callee_return_sscanf": plant(
        "\t(void)sscanf(\"\\001\", \"%c\", "
        "(char *)(uintptr_t)strtoul(\"1073745920\", 0, 0));\n"),
    "L4_literal_sscanf": plant(
        "\t(void)sscanf(\"\\001\", \"%c\", (char *)0x40001000u);\n"),
    "L5_unit_literal_store": plant(
        "\t*(volatile char *)0x40001000u = 1;\n"),
    "L6_neighbour_overrun_sscanf": plant(
        "\t(void)sscanf(\"\\001\\001\\001\\001\\001\", \"%s\", "
        "milan_nbr);\n", "static char milan_nbr[4];\n"),
    "L7_unit_store_neighbour_localptr": plant(
        "\t{ int *p = milan_nbr_i; p[1] = 5; }\n",
        "static int milan_nbr_i[1];\n"),
})

# ---- pin removals (each pin's check disabled in verdict_image_pins / aem_verdict_pins)
def off(old, new):
    return [(TB, old, new)]
VARIANTS.update({
    "K1_no_write_pin": off(
        '        if stores != ["milan_init()"] or \\\n'
        '                writes != [("milan_init", Rv32Tag("call:load_aem_image"))]:\n',
        '        if False:\n'),
    "K2_no_escape_pin": off(
        "        if escapes:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}",
        "        if False:\n            broken.append(f\"{VERDICT_PIN_ESCAPE}"),
    "K3_no_name_pin": off(
        "        if others:\n            broken.append(f\"{VERDICT_PIN_NAME}",
        "        if False:\n            broken.append(f\"{VERDICT_PIN_NAME}"),
    "K4_no_local_pin": off(
        '        if not verdict["local"]:\n            broken.append(VERDICT_PIN_LOCAL)\n',
        '        if False:\n            broken.append(VERDICT_PIN_LOCAL)\n'),
    "K5_no_pcrel_pin": off(
        '        elif image["bare_auipc"]:\n',
        '        elif False:\n'),
    "K6_no_address_pin": off(
        "            if refused is not None:\n                broken.append(f\"{VERDICT_PIN_ADDRESS}",
        "            if False:\n                broken.append(f\"{VERDICT_PIN_ADDRESS}"),
    "K7_no_unit_pin": off(
        "        if naming:\n            broken.append(f\"{VERDICT_PIN_UNIT}",
        "        if False:\n            broken.append(f\"{VERDICT_PIN_UNIT}"),
    "K8_image_store_only_resolved": off(
        '        if stores != ["milan_init()"] or \\\n',
        '        if False or \\\n'),
})

# ---- counterfactual: the head with the +2 and +3 breaks removed (round-4 set)
ONLY_PLUS1 = [(TB,
    "        2: in_nvm_boot(\"static int milan_verdict_next;\\n\",\n"
    "                       \"\\t(void)sscanf(\\\"\\\\001\\\", \\\"%c\\\", \"\n"
    "                       \"(char *)(&milan_verdict_next - 1) + 2);\\n\",\n"
    "                       \"verdict address on interior byte +2\"),\n"
    "        3: in_nvm_boot(\"static int milan_verdict_next;\\n\",\n"
    "                       \"\\t(void)sscanf(\\\"\\\\001\\\", \\\"%c\\\", \"\n"
    "                       \"(char *)(&milan_verdict_next - 1) + 3);\\n\",\n"
    "                       \"verdict address on interior byte +3\"),\n",
    "")]
VARIANTS.update({
    "C0_only_plus1": ONLY_PLUS1,
    "C2_only_plus1_ref_first2": ONLY_PLUS1 + ref_prefix(2),
    "C3_only_plus1_ref_first3": ONLY_PLUS1 + ref_prefix(3),
    "C4_only_plus1_drop_byte2": ONLY_PLUS1 + drop_ref_byte(2),
})

# ---- counterfactual: no interior break at all (round-3 set of 14)
VARIANTS.update({
    "C1_no_interior_ref_first1": [(TB,
        "           planted, None)\n          for offset, planted in verdict_interior_breaks.items()),\n",
        "           planted, None)\n          for offset, planted in verdict_interior_breaks.items() if False),\n"),
        (TB, "        for offset, planted in verdict_interior_breaks.items():\n            _image",
             "        for offset, planted in ():\n            _image")] + ref_prefix(1),
})


def make_variant(name, edits):
    dst = SCRATCH / "v" / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(BASE, dst, symlinks=True)
    by_file = {}
    for path, old, new in edits:
        by_file.setdefault(path, []).append((old, new))
    by_file.setdefault(TB, [])
    for path, pairs in by_file.items():
        target = dst / path
        text = target.read_text(encoding="utf-8")
        for old, new in pairs:
            text = edit(text, old, new, label=f"{name}:{path}")
        if path == TB:
            text = hooked(text)
        target.write_text(text, encoding="utf-8")
    return dst


if __name__ == "__main__":
    name = sys.argv[1]
    tree = make_variant(name, VARIANTS[name])
    print(f"variant {name} at {tree}", flush=True)
