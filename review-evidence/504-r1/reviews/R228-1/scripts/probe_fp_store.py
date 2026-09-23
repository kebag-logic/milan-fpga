#!/usr/bin/env python3
"""Does the RV32 resolver classify every store the ADOPTED compiler emits?

Usage: probe_fp_store.py <clone> <sdk-prefix> <scratch-dir>
Compiles one unit at the census flags (-std=gnu99 -O0 -fno-inline -S) with
the verified SDK twice: with the SDK's own default ISA/ABI (what gate 1b
uses, driver ()), and with an ILP32 soft-float ISA like the previously
supported RV32IMA compiler. Then feeds each assembly to the exact-head
resolver (test_builder.rv32_unit) and lists the stores it reports per
function, beside the store mnemonics actually present in the assembly.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

clone, prefix, scratch = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(clone / "sw/builder"), str(clone / "scripts")]
import test_builder as tb  # noqa: E402

scratch.mkdir(parents=True, exist_ok=True)
unit = scratch / "unit.c"
unit.write_text(
    "#define BASE 0x90000000u\n"
    "void int_store(void) { *(volatile unsigned int *)(BASE + 0x750u) = 1u; }\n"
    "void float_store(void) { *(volatile float *)(BASE + 0x750u) = 1.0f; }\n"
    "void double_store(void) { *(volatile double *)(BASE + 0x614u) = 1.0; }\n"
    "void float_arg(float v) { *(volatile float *)(BASE + 0x750u) = v; }\n"
    "void amo_swap(void) { __atomic_exchange_n((unsigned int *)(BASE + 0x750u), 1u, __ATOMIC_SEQ_CST); }\n"
)
compiler = prefix / "bin/riscv32-linux-gcc"
store_like = re.compile(r"^\s+(f?s[bhwd]|c\.f?s[wd]|sc\.w|amo[a-z]+\.w)\b", re.M)
report = {"compiler_version": subprocess.run([str(compiler), "--version"], capture_output=True,
                                             text=True).stdout.splitlines()[0]}
for label, driver in (("sdk-default (gate 1b driver ())", []),
                      ("ilp32 soft-float rv32ima", ["-march=rv32ima_zicsr", "-mabi=ilp32"])):
    asm = scratch / f"{label.split()[0]}.s"
    built = subprocess.run([str(compiler), *driver, "-std=gnu99", "-O0", "-fno-inline", "-S",
                            "-o", str(asm), str(unit)], capture_output=True, text=True)
    entry = {"argv_tail": driver + ["-std=gnu99", "-O0", "-fno-inline", "-S"],
             "compile_exit": built.returncode}
    if built.returncode == 0:
        text = asm.read_text()
        arch = re.search(r'\.attribute\s+arch,\s*"([^"]+)"', text)
        entry["arch"] = arch.group(1) if arch else None
        resolved = tb.rv32_unit(text)
        per_fn = {}
        for name, run in resolved["runs"].items():
            body = "\n".join(f"\t{m} {o}" for m, o in
                             (insn for block in run["blocks"].values() for insn in block))
            per_fn[name] = {
                "store_mnemonics_in_asm": store_like.findall(body),
                "stores_resolver_reported": [
                    hex(where) if isinstance(where, int) else repr(where)
                    for _block, (where, _value) in run["stores"]],
            }
        entry["functions"] = per_fn
    else:
        entry["stderr"] = built.stderr.strip().splitlines()[-2:]
    report[label] = entry
print(json.dumps(report, indent=1))
