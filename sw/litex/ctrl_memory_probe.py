# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The memory test's firmware probe, shared by its suites and build-only capture."""

from pathlib import Path
import subprocess

import ctrl_memory

PLAT = Path(__file__).resolve().parents[1] / "firmware/ctrl/plat"

PROBE = """\
int counter = 7;
unsigned char nvm_stage[3344];
int main(void) { return counter + nvm_stage[counter]; }
"""


def link(cc: str, tmp: Path, script: str) -> Path:
    """The probe linked by `script` behind the reset entry."""
    (tmp / "regions.ld").write_text(ctrl_memory.regions_ld())
    (tmp / "probe.c").write_text(PROBE)
    (tmp / "split.ld").write_text(script)
    flags = ["-march=rv32i", "-mabi=ilp32"]
    subprocess.run([cc, *flags, "-ffreestanding", "-Os", "-c", str(tmp / "probe.c"), "-o", str(tmp / "probe.o")],
                   check=True)
    subprocess.run([cc, *flags, "-c", str(PLAT / "ctrl_split_start.S"), "-o", str(tmp / "start.o")], check=True)
    elf_path = tmp / "probe.elf"
    subprocess.run([cc, *flags, "-nostdlib", "-static", "-no-pie", "-Wl,--gc-sections,--build-id=none",
                    "-T", str(tmp / "split.ld"), f"-L{tmp}", str(tmp / "start.o"), str(tmp / "probe.o"),
                    "-o", str(elf_path)], check=True)
    return elf_path
