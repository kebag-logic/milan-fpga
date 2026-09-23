# SPDX-License-Identifier: MIT
"""R228-4 whole-gate compiled plants, exec'd INSIDE gate 1b by r228_4_gate_run.py.

The R228-F6 byte-3 plants (unchanged from R228-3) plus the byte-0
reference. Each is spliced at the end of configure_fabric() with the
gate's own helpers and judged by the gate's own assert_boot_contract():
ACCEPTED (the whole boot contract passed it) or REFUSED with the first
line of the refusal. Each byte-3 plant parks an address OUTSIDE the
window, then writes the window's top byte into byte 3 through a union and
stores through the word, so at run time it writes ADP_CTRL.
"""

import json
import os
from pathlib import Path

adp = adp_window_address                      # noqa: F821 (gate local)
page = f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n"  # noqa: F821
blk = "typedef struct { volatile uint32_t ctrl; } *milan_slot_blk;\n"
parked_top = (adp & 0x00FF_FFFF) | 0x8000_0000     # outside the window
assert parked_top != adp


def spliced(label, body, typedefs=""):
    """`body` at the end of configure_fabric(), `typedefs` before it."""
    return replace_once(                                          # noqa: F821
        stored_before_aem("{\n\t\t" + "\n\t\t".join(body) + "\n\t}",  # noqa: F821
                          f"{label} store"),
        "static int aem_loaded;",
        blk + page + typedefs + "\nstatic int aem_loaded;", f"{label} typedef")


probes = (
    ("frame union: byte 3 rewrites a parked address's top byte into ADP_CTRL",
     spliced("byte3", (
         "union { uint32_t word; uint8_t b[4]; } milan_slot;",
         f"milan_slot.word = 0x{parked_top:08x}u;",
         f"milan_slot.b[3] = 0x{adp >> 24:02x}u;",
         "((milan_slot_blk)milan_slot.word)->ctrl = 1u;"))),
    ("static union: byte 3 rewrites a parked address's top byte into ADP_CTRL",
     spliced("static byte3", (
         f"milan_park_u.word = 0x{parked_top:08x}u;",
         f"milan_park_u.b[3] = 0x{adp >> 24:02x}u;",
         "((milan_slot_blk)milan_park_u.word)->ctrl = 1u;"),
         "static union { uint32_t word; uint8_t b[4]; } milan_park_u;\n")),
    ("frame union: byte 0 rewrite (positive reference)",
     spliced("byte0", (
         "union { uint32_t word; uint8_t low; } milan_slot;",
         f"milan_slot.word = (csr_page << 16) | {adp_name};",   # noqa: F821
         f"milan_slot.low = 0x{adp & 0xFF:02x}u;",
         "((milan_slot_blk)milan_slot.word)->ctrl = 1u;"))),
)

verdicts = []
for label, firmware in probes:
    try:
        assert_boot_contract(firmware, docs_source, csr_source)  # noqa: F821
    except (AssertionError, ValueError) as exc:
        verdicts.append({"probe": label, "verdict": "REFUSED",
                         "reason": str(exc).splitlines()[0][:600]})
    else:
        verdicts.append({"probe": label, "verdict": "ACCEPTED", "reason": None})
    taken = census_take(firmware, label)                          # noqa: F821
    lines = (taken.get("text") or "").splitlines()
    start = max((i for i, line in enumerate(lines)
                 if line.startswith("configure_fabric:")), default=0)
    verdicts[-1]["arch"] = taken.get("arch")
    verdicts[-1]["configure_fabric_tail_mem_ops"] = [
        line for line in lines[start:start + 400]
        if any(k in line for k in ("sb\t", "sw\t", "lbu\t", "lw\t", "call\t"))][-16:]
    print(f"R228 PROBE {verdicts[-1]['verdict']}: {label}", flush=True)
Path(os.environ["R228_PROBE_OUT"]).write_text(json.dumps(verdicts, indent=1) + "\n")
