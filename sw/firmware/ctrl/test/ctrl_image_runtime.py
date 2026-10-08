#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build the size fixture's small bare-metal runtime from external sources.

No source or installed package is modified. The manifest records each compiled
source, included dependency, command and archive for independent reproduction.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from ctrl_build import Refusal
import fw_rv32


def main() -> int:
    """Compile only memory primitives and integer arithmetic helpers."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--picolibc", type=Path, required=True)
    parser.add_argument("--compiler-rt", type=Path, required=True)
    parser.add_argument("--litex-software", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cc = fw_rv32.compiler()
    if cc is None:
        raise Refusal("the pinned RV32 compiler is required")
    pico = args.picolibc.resolve()
    crt = args.compiler_rt.resolve() / "lib/builtins"
    lite = args.litex_software.resolve()
    config = lite / "libc/picolibc-minimal.h"
    (out / "picolibc.h").write_bytes(config.read_bytes())
    flags = ["-march=rv32i", "-mabi=ilp32", "-Os", "-ffreestanding", "-fno-pie",
             "-fno-common", "-ffunction-sections", "-fdata-sections", "-fno-builtin",
             "-nostdlib", "-MMD", "-I" + str(out), "-I" + str(pico / "libc/include"),
             "-include", str(out / "picolibc.h")]
    helpers = ("umodsi3 udivsi3 divsi3 modsi3 lshrdi3 muldi3 divdi3 ashldi3 ashrdi3 "
               "udivmoddi4 clzsi2 ctzsi2 clzdi2 ctzdi2 udivdi3 umoddi3 moddi3 ucmpdi2").split()
    groups = [
        ("libc.a", [pico / "libc/string" / (name + ".c")
                    for name in ("memcpy", "memmove", "memset", "memcmp")],
         ["-D_LIBC", *["-I" + str(pico / name) for name in
                      ("libc/string", "libc/locale", "libc/ctype", "libm/common")]]),
        ("libcompiler_rt.a", [crt / (name + ".c") for name in helpers] +
         [lite / "libcompiler_rt/mulsi3.c"],
         ["-D_YUGA_LITTLE_ENDIAN=1", "-D_YUGA_BIG_ENDIAN=0"]),
    ]
    files = {config}
    commands = []
    for library, sources, includes in groups:
        objects = []
        for src in sources:
            obj = out / (src.stem + ".o")
            command = [cc, *flags, *includes, "-c", str(src), "-o", str(obj)]
            subprocess.run(command, check=True)
            commands.append(command)
            objects.append(obj)
            dependencies = obj.with_suffix(".d").read_text().replace("\\\n", "").split(":", 1)[1]
            files.update(Path(name) for name in dependencies.split())
        findings = fw_rv32.object_findings(cc, objects)
        if findings:
            raise Refusal(str(findings))
        archive = out / library
        archive.unlink(missing_ok=True)
        command = [cc.removesuffix("gcc") + "ar", "crs", str(archive), *map(str, objects)]
        subprocess.run(command, check=True)
        commands.append(command)
        files.add(archive)
    records = [{"path": str(path), "size": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(files)]
    (out / "provenance.json").write_text(json.dumps({"files": records, "commands": commands}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
