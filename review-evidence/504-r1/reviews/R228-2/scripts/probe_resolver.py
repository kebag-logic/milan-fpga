#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned, independent probe of the RV32 store resolver at a head.

Compiles small C units with the selected SDK at the census flags
(-std=gnu99 -O0 -fno-inline -S, no -march: the SDK default ISA, as the
census does) and feeds each emitted function to the resolver's module-level
entry points (rv32_functions / rv32_run). For every planted store into a
test window word it reports whether the resolver makes it VISIBLE:
  - a resolved int or bounded range touching the window word  -> CAUGHT
  - an unplaceable Rv32Where (not stack, not sym)               -> CAUGHT
    (rule 1b refuses any unplaced class the residual does not name)
  - nothing touching the window                                  -> MISSED
It also runs hand-written assembly edge cases.

Usage: probe_resolver.py <repo> <sdk-compiler> <out.json>
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO, CC, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(REPO / "sw/builder"))
import test_builder as tb  # noqa: E402

PAGE = 0x9000
WORD = 0x9000_0600          # the planted window word
LO, HI = 0x9000_0000, 0x9001_0000   # test window used for classification

PRELUDE = f"""
#include <stdint.h>
static unsigned int page = 0x{PAGE:04x}u;
#define W ((page << 16) | 0x600u)
"""

C_CASES = {
    "int-sw": "void f(void){ *(volatile uint32_t *)W = 1u; }",
    "float-overlay-fsw":
        "typedef struct { volatile float c; } *fb;\n"
        "void f(void){ ((fb)W)->c = 1.0000001f; }",
    "double-overlay-fsd":
        "typedef struct { volatile double c; } *db;\n"
        "void f(void){ ((db)W)->c = 1.0000000000000002; }",
    "double-straddle-below-word":
        "void f(void){ *(volatile double *)(W - 4u) = 1.5; }",
    "float-compound-add":
        "typedef struct { volatile float c; } *fb;\n"
        "void f(void){ ((fb)W)->c += 1.0f; }",
    "complex-float":
        "void f(void){ *(volatile _Complex float *)W = 1.0f; }",
    "long-double":
        "void f(void){ *(volatile long double *)W = 1.0L; }",
    "struct-of-doubles-copy":
        "struct s { double a, b; };\n"
        "void f(void){ struct s v = { 1.5, 2.5 }; *(volatile struct s *)(W - 8u) = v; }",
    "atomic-exchange-32":
        "void f(void){ (void)__atomic_exchange_n((volatile uint32_t *)W, 1u, __ATOMIC_SEQ_CST); }",
    "atomic-fetch-or-32":
        "void f(void){ (void)__atomic_fetch_or((volatile uint32_t *)W, 1u, __ATOMIC_RELAXED); }",
    "atomic-fetch-and-32":
        "void f(void){ (void)__atomic_fetch_and((volatile uint32_t *)W, 1u, __ATOMIC_ACQ_REL); }",
    "atomic-cas-32":
        "void f(void){ uint32_t e = 0u; (void)__atomic_compare_exchange_n((volatile uint32_t *)W, &e, 1u, 0, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST); }",
    "atomic-cas-weak-32":
        "void f(void){ uint32_t e = 0u; (void)__atomic_compare_exchange_n((volatile uint32_t *)W, &e, 1u, 1, __ATOMIC_RELAXED, __ATOMIC_RELAXED); }",
    "atomic-store-32":
        "void f(void){ __atomic_store_n((volatile uint32_t *)W, 1u, __ATOMIC_SEQ_CST); }",
    "sync-test-and-set":
        "void f(void){ (void)__sync_lock_test_and_set((volatile uint32_t *)W, 1u); }",
    "sync-fetch-and-or":
        "void f(void){ (void)__sync_fetch_and_or((volatile uint32_t *)W, 1u); }",
    "atomic-fetch-or-8":
        "void f(void){ (void)__atomic_fetch_or((volatile uint8_t *)W, 1u, __ATOMIC_SEQ_CST); }",
    "atomic-exchange-16":
        "void f(void){ (void)__atomic_exchange_n((volatile uint16_t *)W, 1u, __ATOMIC_SEQ_CST); }",
    "atomic-exchange-64-libcall":
        "void f(void){ (void)__atomic_exchange_n((volatile uint64_t *)W, 1u, __ATOMIC_SEQ_CST); }",
    "builtin-memset-libcall":
        "void f(void){ __builtin_memset((void *)W, 1, 1); }",
    "builtin-memcpy-4":
        "void f(void){ uint32_t one = 1u; __builtin_memcpy((void *)W, &one, 4); }",
    "union-fp-over-parked-outside":
        "union u { uint32_t w; float f; };\n"
        "void f(float g){ union u v; v.w = 0x80001000u; v.f = g; *(volatile uint32_t *)v.w = 1u; }",
    "union-byte-over-parked-outside":
        "union u { uint32_t w; uint8_t b[4]; };\n"
        "void f(void){ union u v; v.w = 0x80001000u; v.b[3] = 0x90u; *(volatile uint32_t *)v.w = 1u; }",
    "union-double-over-parked-outside":
        "union u { uint32_t w[2]; double d; };\n"
        "void f(double g){ union u v; v.w[1] = 0x80001000u; v.d = g; *(volatile uint32_t *)v.w[1] = 1u; }",
    "bounded-loop-fsd":
        "void f(void){ for (unsigned i = 0; i < 4u; i++) ((volatile double *)(W - 16u))[i] = 0.5; }",
}

ASM_CASES = {
    # hand-written, one resolved base in a4 = WORD
    "asm-fsq": "\tfsq fa5,0(a4)\n",
    "asm-fsh": "\tfsh fa5,2(a4)\n",
    "asm-amomax-aq": "\tamomax.w.aq a3,a5,(a4)\n",
    "asm-amominu-rl": "\tamominu.w.rl zero,a5,0(a4)\n",
    "asm-amoswap-d-rv64-only": "\tamoswap.d a3,a5,0(a4)\n",
    "asm-amoadd-b-zabha": "\tamoadd.b a3,a5,0(a4)\n",
    "asm-amocas-w-zacas": "\tamocas.w a3,a5,0(a4)\n",
    "asm-cbo-zero": "\tcbo.zero (a4)\n",
    "asm-cbo-zero-0": "\tcbo.zero 0(a4)\n",
    "asm-c-sw": "\tc.sw a5,0(a4)\n",
    "asm-c-fsw": "\tc.fsw fa5,0(a4)\n",
    "asm-c-fsd": "\tc.fsd fa5,0(a4)\n",
    "asm-vse32": "\tvse32.v v1,(a4)\n",
    "asm-sw-spaced-operand": "\tsw a5, 0( a4 )\n",
    "asm-fsw-pcrel-lo": "\tfsw fa5,%pcrel_lo(.L1)(a4)\n",
    "asm-sc-w-no-disp": "\tsc.w a0,a5,(a4)\n",
    "asm-sc-w-aqrl": "\tsc.w.aqrl a0,a5,(a4)\n",
    "asm-sw-hex-disp": "\tsw a5,0x0(a4)\n",
    "asm-fsd-neg-disp-straddle": "\taddi a4,a4,4\n\tfsd fa5,-8(a4)\n",
}


def classify(stores):
    """CAUGHT if any reported store touches WORD or is an unplaceable class."""
    touched, where = [], []
    for _at, (address, _value) in stores:
        if isinstance(address, int):
            # every written word is reported, so a store covering WORD
            # reports an address inside [WORD, WORD + 3]
            if WORD <= address <= WORD + 3:
                touched.append(f"0x{address:08x}")
        elif isinstance(address, tb.Rv32Range):
            if address.lo <= WORD + 3 and address.hi >= WORD:
                touched.append(repr(address))
        elif isinstance(address, tb.Rv32Where):
            if address.kind not in ("stack", "sym"):
                where.append(repr(address))
    return touched, where


def render(stores):
    out = []
    for _at, (address, _value) in stores:
        out.append(f"0x{address:08x}" if isinstance(address, int) else repr(address))
    return out


def main():
    results = {}
    with tempfile.TemporaryDirectory(prefix="r228-probe-") as tmp:
        tmp = Path(tmp)
        for name, body in C_CASES.items():
            src = tmp / f"{name}.c"
            asm = tmp / f"{name}.s"
            src.write_text(PRELUDE + body + "\n")
            built = subprocess.run([CC, "-std=gnu99", "-O0", "-fno-inline",
                                    "-S", "-o", str(asm), str(src)],
                                   capture_output=True, text=True)
            if built.returncode != 0:
                results[name] = {"compile": "FAILED",
                                 "stderr": built.stderr.strip().splitlines()[-3:]}
                continue
            text = asm.read_text()
            funcs = tb.rv32_functions(text)
            run = tb.rv32_run(funcs["f"], {"page": PAGE})
            touched, where = classify(run["stores"])
            mnems = sorted({line.split()[0] for line in text.splitlines()
                            if line.startswith("\t") and not line.startswith("\t.")
                            and line.split()})
            calls = [callee for _at, (callee, _h) in run["calls"]]
            results[name] = {
                "verdict": "CAUGHT" if (touched or where) else "MISSED",
                "window_hits": touched, "unplaceable": where,
                "reported": render(run["stores"]), "calls": calls,
                "mnemonics": mnems,
            }
        for name, body in ASM_CASES.items():
            text = f"f:\n\tli a4,{tb._rv32_s32(WORD)}\n{body}\tret\n"
            try:
                run = tb.rv32_run(tb.rv32_functions(text)["f"], {})
                touched, where = classify(run["stores"])
                results[name] = {"verdict": "CAUGHT" if (touched or where) else "MISSED",
                                 "window_hits": touched, "unplaceable": where,
                                 "reported": render(run["stores"])}
            except Exception as exc:  # a crash is a result too
                results[name] = {"verdict": "ERROR", "error": repr(exc)}
        # loads must not be reported as stores
        for name, body in {"loads-flw-fld-lrw-lw": "\tflw fa5,0(a4)\n\tfld fa4,0(a4)\n\tlr.w a3,(a4)\n\tlw a2,0(a4)\n",
                           "load-flq": "\tflq fa5,0(a4)\n",
                           "load-lr-w-aqrl": "\tlr.w.aqrl a3,0(a4)\n"}.items():
            text = f"f:\n\tli a4,{tb._rv32_s32(WORD)}\n{body}\tret\n"
            run = tb.rv32_run(tb.rv32_functions(text)["f"], {})
            results[name] = {"verdict": "NO-STORE" if not run["stores"] else "REPORTED",
                             "reported": render(run["stores"])}
    OUT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    width = max(map(len, results))
    for name, rec in results.items():
        print(f"{name:<{width}}  {rec.get('verdict', rec.get('compile'))}  "
              f"{rec.get('window_hits', '')} {rec.get('unplaceable', '')} "
              f"calls={rec.get('calls', '')}")


if __name__ == "__main__":
    main()
