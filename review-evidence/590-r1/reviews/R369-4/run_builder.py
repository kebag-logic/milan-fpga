#!/usr/bin/env python3
"""Run sw/builder/test_builder.py in-process with an audited RV32 compiler mode.

Usage (from the checkout root):
  run_builder.py --sdk <verified SDK host dir> --audit <jsonl> [builder args...]
  run_builder.py --absent --audit <jsonl> [builder args...]

--sdk maps only argv[0] of the builder's absolute selector
($HOME/br-milan-rv32/host/bin/riscv32-linux-gcc) onto the verified SDK's
compiler; every other argument and option is preserved and logged.
--absent makes every cross candidate raise FileNotFoundError, as if the
compilers were not installed. Remaining argv is passed to the builder.
"""
import json
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

SELECTOR = str(Path.home() / "br-milan-rv32/host/bin/riscv32-linux-gcc")
CROSS = {SELECTOR, "riscv64-elf-gcc", "riscv32-unknown-elf-gcc"}


def main() -> None:
    args = sys.argv[1:]
    mode = args.pop(0)
    sdk = Path(args.pop(0)) if mode == "--sdk" else None
    assert args.pop(0) == "--audit"
    audit = Path(args.pop(0))
    if sdk is not None:
        subprocess.run([sys.executable, "scripts/ci_rv32_sdk.py", "--destination",
                        str(sdk), "--verify-only"], check=True)
    real_run = subprocess.run
    stream = audit.open("w")
    counts = {"mapped": 0, "hidden": 0}

    def audited(argv, *a, **kw):
        if isinstance(argv, (list, tuple)) and argv and str(argv[0]) in CROSS:
            requested = [str(x) for x in argv]
            if sdk is None:
                counts["hidden"] += 1
                stream.write(json.dumps({"requested": requested, "executed": None}) + "\n")
                stream.flush()
                raise FileNotFoundError(f"deliberately absent: {requested[0]}")
            if requested[0] == SELECTOR:
                actual = [str(sdk / "bin/riscv32-linux-gcc"), *requested[1:]]
                result = real_run(actual, *a, **kw)
                counts["mapped"] += 1
                stream.write(json.dumps({"requested": requested, "executed": actual,
                                         "rc": result.returncode}) + "\n")
                stream.flush()
                return result
        return real_run(argv, *a, **kw)

    print(f"mode={mode} sdk={sdk} audit={audit} builder_argv={args}", flush=True)
    sys.path.insert(0, str(Path("sw/builder").resolve()))
    code = 0
    with patch("subprocess.run", audited), \
            patch.object(sys, "argv", ["sw/builder/test_builder.py", *args]):
        try:
            runpy.run_path("sw/builder/test_builder.py", run_name="__main__")
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    stream.close()
    print(f"compiler calls: {counts}", flush=True)
    if sdk is not None:
        assert counts["mapped"] > 0, "no mapped SDK compiler call"
    else:
        assert counts["hidden"] > 0, "no cross candidate was hidden"
    sys.exit(code)


if __name__ == "__main__":
    main()
