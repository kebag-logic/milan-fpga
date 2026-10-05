#!/usr/bin/env python3
"""Reviewer probe (R500-4): compile the LiteSPI port and the store for RV32I
freestanding (-Werror) at the Arty clock 83,333,000 Hz and at 100 MHz, with
headers written by the head's own bench helpers for endstation_arty_current,
and list the undefined symbols (libgcc helpers the 64-bit conversion needs).
Usage: probe_rv32_clock.py <clone> <workdir> <rv32-gcc>"""
import subprocess
import sys
from pathlib import Path

clone, work, cc = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(clone / "sw/firmware/ctrl_nvm/test"))
import nvm_bench as nb        # noqa: E402
import nvm_rv32               # noqa: E402

inputs = nb.shape_inputs(clone / "configs/endstation_arty_current.yaml", work / "in")
header = nb.shape_header(inputs.shape, inputs.donor, inputs.ident)
rc = 0
for hz in (83_333_000, 100_000_000):
    gen = work / f"gen{hz}"
    nb.write_headers(gen, header, hz)
    for src in ("plat/nvm_flash_litespi.c", "nvm_store.c", "nvm_klj2.c"):
        obj = work / f"{hz}_{Path(src).stem}.o"
        r = subprocess.run([cc, *nvm_rv32.RV32_FLAGS, f"-I{gen}",
                            f"-I{clone / 'sw/firmware/ctrl_nvm/test/rv32'}", "-c",
                            str(clone / "sw/firmware/ctrl_nvm" / src), "-o", str(obj)],
                           capture_output=True, text=True)
        und = ""
        if r.returncode == 0:
            und = subprocess.run([cc.removesuffix("gcc") + "nm", "-u", str(obj)],
                                 capture_output=True, text=True).stdout.split()
            und = " ".join(x for x in und if x != "U")
        print(f"hz={hz} {src}: rc={r.returncode} undefined=[{und}] {r.stderr.strip()[:300]}")
        rc |= r.returncode
print(f"config clock={inputs.clock_hz}")
sys.exit(rc)
