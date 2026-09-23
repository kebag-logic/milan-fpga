#!/usr/bin/env python3
"""Capture the census compiles (source, assembly, argv) that gate 1b makes.

Usage: capture_census.py <checkout> <sdk-prefix> <out-dir> [count]

Maps only the absolute selector's argv[0] to <sdk-prefix>, the way the
lane's sw/builder/test_firmware_compiler.py does, and stops the gate after
<count> census assemblies were copied (default: run the whole gate). The
checkout is only read; build output goes under <out-dir>/build.
"""
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

checkout, prefix, out = (Path(a).resolve() for a in sys.argv[1:4])
count = int(sys.argv[4]) if len(sys.argv) > 4 else 0
sys.path.insert(0, str(checkout / "sw/builder"))
sys.path.insert(0, str(checkout / "scripts"))
import test_builder as builder  # noqa: E402

selector = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
real_run = subprocess.run
out.mkdir(parents=True, exist_ok=True)
seen = []


class Done(Exception):
    """Raised once enough census compiles were copied."""


def run(argv, **kwargs):
    argv = [str(a) for a in argv]
    if argv and argv[0] == selector:
        argv[0] = str(prefix / "bin/riscv32-linux-gcc")
    result = real_run(argv, **kwargs)
    if "-S" in argv and "-std=gnu99" in argv and result.returncode == 0:
        asm = Path(argv[argv.index("-o") + 1])
        src = Path(argv[-1])
        n = len(seen)
        shutil.copy(asm, out / f"census-{n}.s")
        shutil.copy(src, out / f"census-{n}.c")
        (out / f"census-{n}.argv").write_text(" ".join(argv) + "\n")
        seen.append(asm)
        if count and len(seen) >= count:
            raise Done()
    return result


with patch.object(subprocess, "run", side_effect=run), \
        patch.object(sys, "argv", ["capture", "--require-rv32"]), \
        patch.object(builder, "OUT", out / "build"), \
        patch.object(builder, "SKIPPED", []):
    try:
        builder.test_baremetal_profile_contract()
    except Done:
        pass
print(f"captured {len(seen)} census compile(s) into {out}")
