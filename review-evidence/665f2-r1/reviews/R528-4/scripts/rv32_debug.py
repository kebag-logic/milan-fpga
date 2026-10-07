#!/usr/bin/env python3
"""Debug-profile (assertions enabled) RV32 object compile of the ctrl sources.

Usage: MILAN_RV32_CC=<pinned riscv32-linux-gcc> rv32_debug.py <repo> <outdir>

Uses the repository's own RV32_FLAGS with only -DNDEBUG removed, the gate's
freestanding include set (fw_rv32.includes) and include dirs, for maap/maap.c
alone and for the whole PORTABLE set plus plat/mbx_plat_mmio.c. Reports ELF
class/machine/ABI flags, the RV32 arch attribute, and undefined symbols, and
checks them against the gate's RV32_LIBC and fw_rv32.HELPERS allowances.
"""
import json, os, subprocess, sys
from pathlib import Path

repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest"), str(repo / "scripts")]
import ctrl_build, fw_rv32  # noqa: E402

cc = fw_rv32.compiler()
flags = [f for f in ctrl_build.RV32_FLAGS if f != "-DNDEBUG"]
inc = fw_rv32.includes(cc) + [x for d in ctrl_build.INCLUDE_DIRS for x in ("-I", str(ctrl_build.CTRL / d))]
out.mkdir(parents=True, exist_ok=True)
tool = cc.removesuffix("gcc")
report = {"cc": cc, "cc_version": subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()[0],
          "flags": flags, "sets": {}}
ok = True
for name, srcs in (("maap_only", ["maap/maap.c"]),
                   ("all_twelve", list(ctrl_build.PORTABLE) + ["plat/mbx_plat_mmio.c"])):
    objs, failures = [], []
    for s in srcs:
        o = out / f"{name}_{s.replace('/', '_')}.o"
        r = subprocess.run([cc, *flags, *inc, "-c", str(ctrl_build.CTRL / s), "-o", str(o)], capture_output=True, text=True)
        if r.returncode:
            failures.append(f"{s}: {r.stderr.strip()}")
            continue
        objs.append(o)
    und = set()
    defined = set()
    for o in objs:
        for line in subprocess.run([tool + "nm", str(o)], capture_output=True, text=True).stdout.splitlines():
            p = line.split()
            if len(p) == 2 and p[0] == "U":
                und.add(p[1])
            elif len(p) == 3:
                defined.add(p[2])
    open_syms = sorted(und - defined)
    stray = sorted(set(open_syms) - ctrl_build.RV32_LIBC - fw_rv32.HELPERS)
    abi = fw_rv32.object_findings(cc, objs)
    size = subprocess.run([tool + "size", "-t", *map(str, objs)], capture_output=True, text=True).stdout.strip().splitlines()
    report["sets"][name] = {"sources": srcs, "compile_failures": failures, "objects": len(objs), "undefined": open_syms,
                            "outside_allowance": stray, "abi_findings": abi, "size_total": size[-1] if size else None,
                            "assert_fail_referenced": "__assert_fail" in open_syms}
    ok = ok and not failures and not stray and not abi
print(json.dumps(report, indent=1))
sys.exit(0 if ok else 1)
