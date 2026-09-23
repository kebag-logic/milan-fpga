# SPDX-License-Identifier: MIT
"""R228-3 whole-gate compiled probes, exec'd INSIDE gate 1b by r228_gate_run.py.

Runs after the gate has built every local it needs and just before its
mutation loop. Each probe is a firmware mutant spliced at the end of
configure_fabric() with the gate's own helpers, handed to the gate's own
assert_boot_contract() over the unchanged docs and CSR sources, and its
verdict recorded: ACCEPTED (the whole boot contract passed it) or REFUSED
with the first line of the refusal. Every probe really writes bit 0 of
ADP_CTRL before the AEM verdict when compiled for the product.
"""

import json
import os
from pathlib import Path

adp = adp_window_address                      # noqa: F821 (gate local)
page = f"static unsigned int csr_page = 0x{csr_base >> 16:04x}u;\n"  # noqa: F821
blk = "typedef struct { volatile uint32_t ctrl; } *milan_slot_blk;\n"
assert (adp & 0x00FF_FFFF) | 0x8000_0000 != adp


def spliced(label, body, typedefs=""):
    """`body` at the end of configure_fabric(), `typedefs` before it."""
    return replace_once(                                          # noqa: F821
        stored_before_aem("{\n\t\t" + "\n\t\t".join(body) + "\n\t}",  # noqa: F821
                          f"{label} store"),
        "static int aem_loaded;",
        blk + page + typedefs + "\nstatic int aem_loaded;", f"{label} typedef")


parked_top = (adp & 0x00FF_FFFF) | 0x8000_0000     # outside the window
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
    ("frame union: byte 0 rewrite, the PR's own shape (positive reference)",
     spliced("byte0", (
         "union { uint32_t word; uint8_t low; } milan_slot;",
         f"milan_slot.word = (csr_page << 16) | {adp_name};",   # noqa: F821
         f"milan_slot.low = 0x{adp & 0xFF:02x}u;",
         "((milan_slot_blk)milan_slot.word)->ctrl = 1u;"))),
    ("DOCUMENTED LIMIT: byte LOAD from a frame slot reads the whole word",
     spliced("byte load", (
         "union { uint32_t word; uint8_t low; } milan_slot;",
         "milan_slot.word = 0x40000000u;",
         f"((milan_slot_blk)((csr_page << 16) | ({adp_name} + milan_slot.low)))->ctrl = 1u;"))),  # noqa: E501,F821
    ("DOCUMENTED LIMIT: a callee this unit defines writes the caller's local",
     spliced("callee", (
         "uint32_t milan_slot = 0x80001000u;",
         "milan_park(&milan_slot);",
         "((milan_slot_blk)milan_slot)->ctrl = 1u;"),
         "static void milan_park(uint32_t *slot)\n{\n\t*slot = (csr_page << 16) | "
         f"{adp_name};\n}}\n")),                                 # noqa: F821
    ("DOCUMENTED LIMIT: __builtin_memset onto ADP_CTRL",
     spliced("memset", (
         f"__builtin_memset((void *)((csr_page << 16) | {adp_name}), 1, 1);",),)),  # noqa: F821
    ("DOCUMENTED LIMIT (typedef spelling): memset onto ADP_CTRL",
     spliced("memset typedef", (
         f"__builtin_memset((milan_slot_blk)((csr_page << 16) | {adp_name}), 1, 4);",),)),  # noqa: E501,F821
    ("DOCUMENTED LIMIT (typedef spelling): 64-bit atomic exchange onto ADP_CTRL",
     spliced("u64 atomic typedef", (
         f"(void)__atomic_exchange_n((milan_u64_p)((csr_page << 16) | {adp_name}), "  # noqa: F821
         "1ull, __ATOMIC_SEQ_CST);",),
         "typedef volatile uint64_t *milan_u64_p;\n")),
    ("DOCUMENTED LIMIT (member spelling): a callee writes the caller's local",
     spliced("callee member", (
         "uint32_t milan_slot = 0x80001000u;",
         "milan_park((milan_slot_word_p)&milan_slot);",
         "((milan_slot_blk)milan_slot)->ctrl = 1u;"),
         "typedef struct { uint32_t word; } *milan_slot_word_p;\n"
         "static void milan_park(milan_slot_word_p slot)\n{\n\tslot->word = (csr_page << 16) | "
         f"{adp_name};\n}}\n")),                                 # noqa: F821
    ("sub-word atomic fetch-or, typedef spelling (LR/SC loop with numeric labels)",
     spliced("subword atomic typedef", (
         f"(void)__atomic_fetch_or((milan_u8_p)((csr_page << 16) | {adp_name}), "  # noqa: F821
         "(uint8_t)1u, __ATOMIC_RELAXED);",),
         "typedef volatile uint8_t *milan_u8_p;\n")),
    ("sub-word atomic fetch-or on ADP_CTRL's low byte (LR/SC loop)",
     spliced("subword atomic", (
         f"(void)__atomic_fetch_or((volatile uint8_t *)((csr_page << 16) | {adp_name}), "  # noqa: F821
         "(uint8_t)1u, __ATOMIC_RELAXED);",))),
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
    snippet = []
    if taken.get("text"):
        lines = taken["text"].splitlines()
        start = max((i for i, line in enumerate(lines)
                     if line.startswith("configure_fabric:")), default=0)
        body = lines[start:start + 400]
        snippet = [line for line in body
                   if any(key in line for key in ("sb\t", "sw\t", "lbu\t", "lw\t",
                                                  "lr.w", "sc.w", "call\t", "slli", "or\t"))][-24:]
    verdicts[-1]["arch"] = taken.get("arch")
    verdicts[-1]["configure_fabric_tail_mem_ops"] = snippet
    print(f"R228 PROBE {verdicts[-1]['verdict']}: {label}", flush=True)
Path(os.environ["R228_PROBE_OUT"]).write_text(json.dumps(verdicts, indent=1) + "\n")
