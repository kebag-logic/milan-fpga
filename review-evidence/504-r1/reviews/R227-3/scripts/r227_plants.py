# SPDX-License-Identifier: MIT
"""R227-3 compiled plants, run INSIDE gate 1b's own scope.

Injected into a disposable copy of sw/builder/test_builder.py right after the
store-class compiled loop, where census_take(), assert_resolved_boot_flow()
and assert_boot_contract() are in scope. Each plant is compiled once by the
adopted SDK (through the audited argv[0] mapping), asked of the resolver
alone, and asked of the WHOLE gate (text rules plus instruments). Results go
to the JSON file named by R227_PLANTS_OUT. Nothing here edits the repository.
"""
import json
import os
import re


def _outcome(call):
    try:
        call()
    except (AssertionError, ValueError) as exc:
        text = " ".join(str(exc).split())
        return {"verdict": "REFUSED", "reason": text[:400]}
    return {"verdict": "ACCEPTED", "reason": None}


def run(scope):
    g = scope
    stored_before_aem, replace_once = g["stored_before_aem"], g["replace_once"]
    firmware_source, docs_source = g["firmware_source"], g["docs_source"]
    csr_source, adp_name = g["csr_source"], g["adp_name"]
    csr_base, csr_size = g["csr_base"], g["csr_size"]
    adp = g["adp_window_address"]
    census_take = g["census_take"]
    resolved = g["assert_resolved_boot_flow"]
    whole = g["assert_boot_contract"]
    model = g["source_model"]
    page = csr_base >> 16
    assert csr_base & 0xFFFF == 0 and adp >> 16 == page, \
        (hex(csr_base), hex(adp))
    off = adp & 0xFFFF

    def outside(value):
        return not csr_base <= (value & 0xFFFFFFFF) < csr_base + csr_size

    # A high half that keeps both the parked word and the lattice's
    # misread address outside the window.
    hi = next(h for h in range(0x1234, 0x10000)
              if outside((h << 16) | off) and
              outside((page << 16) | (h << 16) | off))
    parked = (hi << 16) | off
    # For the byte plant: byte 0 real = off >> 8 (0x06 for 0x600), the
    # remaining bytes chosen so the lattice's misread is outside the window.
    assert off & 0xFF == 0, hex(off)
    byte_parked = next(((h << 8) | (off >> 8)) for h in range(0x123456, 0x1000000)
                       if outside(((h << 8) | (off >> 8)) << 8 | (page << 16)) and
                       outside((h << 8) | (off >> 8)))
    blk = "typedef struct { volatile uint32_t ctrl; } *milan_slot_blk;\n"
    page_decl = f"static unsigned int csr_page = 0x{page:04x}u;\n"

    def plant(label, body, extra=""):
        return replace_once(
            stored_before_aem("{\n\t\t" + "\n\t\t".join(body) + "\n\t}", label),
            "static int aem_loaded;",
            blk + extra + page_decl + "\nstatic int aem_loaded;",
            f"{label} typedef")

    plants = {
        # POSITIVE CONTROL: the same union parked word read back WHOLE.
        "control-whole-word-read": plant("control whole-word read", (
            "union { uint32_t word; uint16_t low; } milan_slot;",
            f"milan_slot.word = 0x{parked:08x}u;",
            "((milan_slot_blk)((csr_page << 16) | "
            "(milan_slot.word & 0xffffu)))->ctrl = 1u;")),
        # The read-side sibling of R227-2-F1: a union HALF-WORD read of the
        # parked word at the slot's own offset. Real address: ADP_CTRL.
        "half-word-read-of-frame-slot": plant("half-word read", (
            "union { uint32_t word; uint16_t low; } milan_slot;",
            f"milan_slot.word = 0x{parked:08x}u;",
            "((milan_slot_blk)((csr_page << 16) | milan_slot.low))->ctrl = 1u;")),
        # ... and a BYTE read at the slot's own offset, shifted into place.
        "byte-read-of-frame-slot": plant("byte read", (
            "union { uint32_t word; uint8_t low; } milan_slot;",
            f"milan_slot.word = 0x{byte_parked:08x}u;",
            "((milan_slot_blk)((csr_page << 16) | "
            "((uint32_t)milan_slot.low << 8)))->ctrl = 1u;")),
        # Documented limitation (a callee's write into its caller's frame).
        "callee-writes-caller-frame": plant("callee frame write", (
            "uint32_t milan_slot = 0x80001000u;",
            "milan_fill(&milan_slot);",
            "((milan_slot_blk)milan_slot)->ctrl = 1u;"),
            extra=("typedef struct { uint32_t word; } *milan_slot_word_p;\n"
                   f"static unsigned int milan_fill_page = 0x{page:04x}u;\n"
                   "static void milan_fill(uint32_t *p)\n{\n"
                   "\t((milan_slot_word_p)p)->word = "
                   f"(milan_fill_page << 16) | {adp_name};\n}}\n")),
    }
    # The TOP byte of an aligned word (offset 3): the boundary of
    # _rv32_forget_overlap(). Real word after the byte store: ADP_CTRL.
    assert adp & 0xFF000000 == csr_base & 0xFF000000
    top_parked = next((h << 24) | (adp & 0xFFFFFF) for h in range(0x12, 0x100)
                      if outside((h << 24) | (adp & 0xFFFFFF)))
    plants["top-byte-store-frame"] = plant("top byte store frame", (
        "union { uint32_t word; uint8_t b[4]; } milan_slot;",
        f"milan_slot.word = 0x{top_parked:08x}u;",
        "milan_slot.b[3] = (uint8_t)(csr_page >> 8);",
        "((milan_slot_blk)milan_slot.word)->ctrl = 1u;"))
    plants["top-byte-store-static"] = plant("top byte store static", (
        f"milan_static_slot.word = 0x{top_parked:08x}u;",
        "milan_static_slot.b[3] = (uint8_t)(csr_page >> 8);",
        "((milan_slot_blk)milan_static_slot.word)->ctrl = 1u;"),
        extra="static union { uint32_t word; uint8_t b[4]; } milan_static_slot;\n")
    # Documented (R228-F5) limitations: a library call handed a window pointer.
    plants["doc-64bit-atomic-exchange"] = plant("64-bit atomic exchange", (
        "(void)__atomic_exchange_n((milan_atomic64_p)((csr_page << 16) | "
        f"{adp_name}), 1ull, __ATOMIC_SEQ_CST);",),
        extra="typedef volatile uint64_t *milan_atomic64_p;\n")
    plants["doc-memset"] = plant("memset", (
        f"__builtin_memset((milan_void_p)((csr_page << 16) | {adp_name}), 1, 1);",),
        extra="typedef void *milan_void_p;\n")
    results = {"csr_base": hex(csr_base), "top_parked": hex(top_parked), "csr_size": hex(csr_size),
               "adp_window_address": hex(adp), "parked": hex(parked),
               "byte_parked": hex(byte_parked), "plants": {}}
    for name, source in plants.items():
        taken = census_take(source, name)
        text = taken["text"] or ""
        record = {
            "emits_lhu_frame": bool(re.search(r"(?m)^\s+lhu\s+\w+,-?\d+\(s0\)", text)),
            "emits_lbu_frame": bool(re.search(r"(?m)^\s+lbu\s+\w+,-?\d+\(s0\)", text)),
            "resolver_alone": _outcome(lambda: resolved(text, model, name)),
            "whole_gate": _outcome(lambda: whole(source, docs_source, csr_source,
                                                 None, None, None)),
        }
        results["plants"][name] = record
        print(f"R227-3 PLANT {name}: resolver={record['resolver_alone']['verdict']} "
              f"whole={record['whole_gate']['verdict']}", flush=True)
    with open(os.environ["R227_PLANTS_OUT"], "w") as out:
        json.dump(results, out, indent=1, sort_keys=True)
