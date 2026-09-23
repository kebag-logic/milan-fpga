#!/usr/bin/env python3
"""Run the WHOLE sw/builder/test_builder.py main in one compiler environment.

Evidence driver for the #408/#409 lane (nothing is written into the tree by
this file). The compiler environment is made the way
sw/builder/test_firmware_compiler.py makes it for gate 1b alone:

  --mode sdk     the gate's absolute selector argv[0] is mapped onto the
                 pinned SDK, every other cross candidate is hidden, and the
                 run is given --require-rv32 exactly as both hosted builder
                 consumers are;
  --mode absent  every cross candidate is hidden (FileNotFoundError), the
                 host cc/gcc stay, and no --require-rv32 is passed.

Every compiler-candidate call is logged to --audit as JSON lines.
"""

import argparse
import json
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

LANE = Path("$LANES/408-409-boot-gate-retire")
sys.path.insert(0, str(LANE / "scripts"))
import ci_rv32_sdk as sdk  # noqa: E402

SDK = Path("$VALIDATION_STORAGE/504-manager-r1/sdk-install")
SELECTOR = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
CROSS = {SELECTOR, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("sdk", "absent"), required=True)
    ap.add_argument("--audit", type=Path, required=True)
    ap.add_argument("--source", type=Path,
                    default=LANE / "sw/builder/test_builder.py")
    args = ap.parse_args()
    if args.mode == "sdk":
        sdk.verify(SDK)
    real = subprocess.run
    counts = {"mapped": 0, "hidden": 0}
    with args.audit.open("w") as audit:
        def run(argv, **kwargs):
            first = str(argv[0])
            if first in CROSS:
                if args.mode == "absent" or first != SELECTOR:
                    counts["hidden"] += 1
                    audit.write(json.dumps({"requested": [str(a) for a in argv],
                                            "result": "hidden"}) + "\n")
                    raise FileNotFoundError("deliberately absent RV32 candidate")
                argv = [str(SDK / sdk.COMPILER)] + [str(a) for a in argv[1:]]
                counts["mapped"] += 1
                result = real(argv, **kwargs)
                audit.write(json.dumps({"actual": argv,
                                        "rc": result.returncode}) + "\n")
                audit.flush()
                return result
            return real(argv, **kwargs)

        argv = [str(args.source)] + (["--require-rv32"] if args.mode == "sdk"
                                     else [])
        print(f"run_builder: mode={args.mode} argv={argv[1:]} source={args.source}",
              flush=True)
        try:
            with patch.object(subprocess, "run", side_effect=run), \
                    patch.object(sys, "argv", argv):
                runpy.run_path(str(args.source), run_name="__main__")
        finally:
            print(f"run_builder: selector calls mapped={counts['mapped']} "
                  f"hidden={counts['hidden']}", flush=True)


if __name__ == "__main__":
    main()
