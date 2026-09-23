#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned end-to-end planted-firmware controls.

Copies a checkout (including .git and initialised submodules) to a
disposable destination and plants ONE edit into the shipping firmware
(sw/firmware/milan_baremetal/milan_baremetal.c): a typedef/helper declared
before `static int aem_loaded;` and one statement appended to the end of
configure_fabric(), i.e. on the boot path before the AEM verdict. Each edit
writes the ADP_CTRL word (entity enable) through a paged base, which the
text rules do not see; the question is whether the WHOLE gate 1b refuses it.

Usage: plant_firmware.py <source-checkout> <destination> <mutant-id>
"""

import shutil
import subprocess
import sys
from pathlib import Path

PAGE_DECL = "static unsigned int r228_page = 0x{page:04x}u;\n"
ADDR = "((r228_page << 16) | MILAN_ADP_CTRL)"

MUTANTS = {
    # author-equivalent control: float overlay (fsw)
    "E1-float-overlay": (
        "typedef struct { volatile float ctrl; } *r228_fblk;\n",
        f"((r228_fblk){ADDR})->ctrl = 1.0000001f;"),
    # complex float: two fsw into ADP_CTRL and the next word
    "E3-complex-float": (
        "typedef volatile _Complex float *r228_cfp;\n",
        f"*(r228_cfp){ADDR} = 1.0000001f;"),
    # the same through a member store, a shape the text store set misses
    "E3b-complex-float-member": (
        "typedef struct { volatile _Complex float c; } *r228_cblk;\n",
        f"((r228_cblk){ADDR})->c = 1.0000001f;"),
    # FP read-modify-write: flw, fadd, fsw
    "E4-float-compound": (
        "typedef struct { volatile float ctrl; } *r228_fblk;\n",
        f"((r228_fblk){ADDR})->ctrl += 1.0f;"),
    # sub-word atomic: lr.w/sc.w loop on the aligned word
    "E5-atomic-or-8": (
        "typedef volatile uint8_t *r228_u8p;\n",
        f"(void)__atomic_fetch_or((r228_u8p){ADDR}, 1u, __ATOMIC_SEQ_CST);"),
    # legacy sync builtin: amoswap
    "E6-sync-test-and-set": (
        "typedef volatile uint32_t *r228_u32p;\n",
        f"(void)__sync_lock_test_and_set((r228_u32p){ADDR}, 1u);"),
    # an FP overwrite of a parked outside address, then an integer store
    # through the reloaded word: the stale reading would place it outside
    "E7-union-fp-over-parked": (
        "typedef volatile uint32_t *r228_u32p;\n"
        "union r228_u { uint32_t w; float f; };\n"
        "static float r228_bits(void) { union r228_u v; v.w = "
        f"{ADDR} ; return v.f; }}\n",
        "{ union r228_u v; v.w = 0x80001000u; v.f = r228_bits(); "
        "*(r228_u32p)v.w = 1u; }"),
    # the same, storing through a member of the reloaded word
    "E7b-union-fp-over-parked-member": (
        "typedef struct { volatile uint32_t ctrl; } *r228_blk;\n"
        "union r228_u { uint32_t w; float f; };\n"
        "static float r228_bits(void) { union r228_u v; v.w = "
        f"{ADDR} ; return v.f; }}\n",
        "{ union r228_u v; v.w = 0x80001000u; v.f = r228_bits(); "
        "((r228_blk)v.w)->ctrl = 1u; }"),
    # a byte-indexed double store bounded by its loop, straddling the
    # window's first word from below (0x8FFFFFFB + 8 bytes reaches 0x90000002)
    "E10-ranged-fsd-straddle": (
        "typedef struct { volatile double d; } *r228_dblk;\n",
        "for (unsigned r228_i = 0; r228_i < 12u; r228_i++) "
        "((r228_dblk)(0x8FFFFFF0u + r228_i))->d = 0.5; (void)r228_page;"),
    # a parked outside word in a static's SECOND word, overwritten by an
    # fsd over the whole static, then an integer store through it; at run
    # time the word is the double's high word, 0x90000600 = ADP_CTRL
    "E11-static-fsd-over-second-word": (
        "typedef struct { volatile uint32_t ctrl; } *r228_blk;\n"
        "static union r228_u2 { uint32_t w[2]; double d; } r228_s;\n",
        "{ r228_s.w[1] = 0x80001000u; r228_s.d = -0x1.0060000000001p-767; "
        "((r228_blk)r228_s.w[1])->ctrl = 1u; (void)r228_page; }"),
    # E10 with no window immediate anywhere: the base is a static's word
    "E10b-ranged-fsd-straddle-static-base": (
        "typedef struct { volatile double d; } *r228_dblk;\n"
        "static unsigned int r228_b = 0x8FFFFFF0u;\n",
        "for (unsigned r228_i = 0; r228_i < 12u; r228_i++) "
        "((r228_dblk)(r228_b + r228_i))->d = 0.5; (void)r228_page;"),
    # E11 with no window word in any constant: the double is doubled at run
    # time from a static whose words are 0x00000001 / 0x8FF00600
    "E11b-static-fsd-over-second-word-computed": (
        "typedef struct { volatile uint32_t ctrl; } *r228_blk;\n"
        "static union r228_u2 { uint32_t w[2]; double d; } r228_s;\n"
        "static double r228_half = -0x1.0060000000001p-768;\n",
        "{ r228_s.w[1] = 0x80001000u; r228_s.d = r228_half * 2.0; "
        "((r228_blk)r228_s.w[1])->ctrl = 1u; (void)r228_page; }"),
    # an INTEGER store through a pointer to a local overwrites a parked
    # outside address with ADP_CTRL; the frame slot is not invalidated
    "E12-store-through-local-pointer": (
        "typedef struct { volatile uint32_t ctrl; } *r228_blk;\n"
        "typedef struct { uint32_t w; } *r228_wp;\n",
        "{ uint32_t r228_v = 0x80001000u; r228_wp r228_q = (r228_wp)&r228_v; "
        f"r228_q->w = {ADDR}; ((r228_blk)r228_v)->ctrl = 1u; }}"),
    # the same with an FP store through the local pointer; the float is
    # doubled at run time from a static whose word is 0x8F800600
    "E12f-fp-store-through-local-pointer": (
        "typedef struct { volatile uint32_t ctrl; } *r228_blk;\n"
        "typedef struct { float f; } *r228_fp;\n"
        "static float r228_halff = -0x1.000cp-96f;\n",
        "{ uint32_t r228_v = 0x80001000u; r228_fp r228_q = (r228_fp)&r228_v; "
        "r228_q->f = r228_halff * 2.0f; ((r228_blk)r228_v)->ctrl = 1u; "
        "(void)r228_page; }"),
    # 64-bit atomic exchange: a library call, no store instruction
    "E8-atomic-exchange-64-libcall": (
        "typedef volatile uint64_t *r228_u64p;\n",
        f"(void)__atomic_exchange_n((r228_u64p){ADDR}, 1u, __ATOMIC_SEQ_CST);"),
    # memset over the word: a library call
    "E9-memset-libcall": (
        "typedef volatile uint8_t *r228_u8p;\n",
        f"__builtin_memset((void *)(r228_u8p){ADDR}, 1, 64);"),
    # the same with no spelled pointer cast (typedef only)
    "E9b-memset-libcall-typedef": (
        "typedef uint8_t *r228_u8p;\n",
        f"__builtin_memset((r228_u8p){ADDR}, 1, 64);"),
}


def main() -> None:
    source, destination, mutant = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    decl, statement = MUTANTS[mutant]
    if destination.exists():
        shutil.rmtree(destination)
    subprocess.run(["cp", "-a", str(source), str(destination)], check=True)
    firmware = destination / "sw/firmware/milan_baremetal/milan_baremetal.c"
    text = firmware.read_text()
    # the page is the upper half of MILAN_CSR_BASE in sw/litex/milan_soc.py
    # (0x9000_0000), the window base gate 1b reads for its census
    page = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0x9000
    anchor = "static int aem_loaded;"
    assert text.count(anchor) == 1, "anchor"
    text = text.replace(anchor, PAGE_DECL.format(page=page) + decl + "\n" + anchor, 1)
    tail = "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);\n}"
    assert text.count(tail) == 1, "tail"
    text = text.replace(tail, "\tmilan_write(MILAN_CRF_TX_CTRL, MILAN_CRF_TX_CTRL_BOOT);\n\t"
                        + statement + "\n}", 1)
    firmware.write_text(text)
    print(f"planted {mutant} into {firmware}")


if __name__ == "__main__":
    main()
